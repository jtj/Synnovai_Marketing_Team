from typing import List
from datetime import datetime
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os
import glob
from marketing_posts.llm_wrapper import JSONCleaningLLM

# Uncomment the following line to use an example of a custom tool
# from marketing_posts.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from pydantic import BaseModel, Field

class MarketStrategy(BaseModel):
	"""Market strategy model"""
	name: str = Field(..., description="Name of the market strategy")
	tatics: List[str] = Field(..., description="List of tactics to be used in the market strategy")
	channels: List[str] = Field(..., description="List of channels to be used in the market strategy")
	KPIs: List[str] = Field(..., description="List of KPIs to be used in the market strategy")

class CampaignIdea(BaseModel):
	"""Campaign idea model"""
	name: str = Field(..., description="Name of the campaign idea")
	description: str = Field(..., description="Description of the campaign idea")
	audience: str = Field(..., description="Audience of the campaign idea")
	channel: str = Field(..., description="Channel of the campaign idea")

class Copy(BaseModel):
	"""Copy model"""
	title: str = Field(..., description="Title of the copy")
	body: str = Field(..., description="Body of the copy")

@CrewBase
class MarketingPostsCrew():
	"""MarketingPosts crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# Initialize the Gemini LLM
	# Note: Ensure GEMINI_API_KEY is set in your .env file
	# Initialize the Gemini LLM
	# Note: Ensure GEMINI_API_KEY is set in your .env file
	def __init__(self, model_name="gemini/gemini-pro-latest", output_name="marketing"):
		# Using 'gemini/gemini-pro' as requested. usage of specific 3.0 preview models 
		# requires the specific string e.g. 'gemini/gemini-1.5-pro' or 'gemini/gemini-3.0-pro-preview'
		self.llm = JSONCleaningLLM(model=model_name)
		self.output_name = output_name
		self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
		self.folder_path = f"Reports/{self.timestamp}_{self.output_name}"
		os.makedirs(self.folder_path, exist_ok=True)

	@agent
	def lead_market_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['lead_market_analyst'],
			tools=[SerperDevTool(), ScrapeWebsiteTool()],
			verbose=True,
			memory=False,
			llm=self.llm,
			function_calling_llm=self.llm
		)

	@agent
	def chief_marketing_strategist(self) -> Agent:
		return Agent(
			config=self.agents_config['chief_marketing_strategist'],
			tools=[SerperDevTool(), ScrapeWebsiteTool()],
			verbose=True,
			memory=False,
			llm=self.llm,
			function_calling_llm=self.llm
		)

	@agent
	def creative_content_creator(self) -> Agent:
		return Agent(
			config=self.agents_config['creative_content_creator'],
			verbose=True,
			memory=False,
			llm=self.llm,
			function_calling_llm=self.llm
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			agent=self.lead_market_analyst(),
			output_file=os.path.join(self.folder_path, "lead_market_analyst_research.md")
		)

	@task
	def project_understanding_task(self) -> Task:
		return Task(
			config=self.tasks_config['project_understanding_task'],
			agent=self.chief_marketing_strategist(),
			output_file=os.path.join(self.folder_path, "chief_strategist_project_understanding.md")
		)

	@task
	def marketing_strategy_task(self) -> Task:
		return Task(
			config=self.tasks_config['marketing_strategy_task'],
			agent=self.chief_marketing_strategist(),
			output_json=MarketStrategy,
			output_file=os.path.join(self.folder_path, "chief_strategist_marketing_strategy.md")
		)

	@task
	def campaign_idea_task(self) -> Task:
		return Task(
			config=self.tasks_config['campaign_idea_task'],
			agent=self.creative_content_creator(),
   		output_json=CampaignIdea,
			output_file=os.path.join(self.folder_path, "creative_creator_campaign_ideas.md")
		)

	@task
	def copy_creation_task(self) -> Task:
		return Task(
			config=self.tasks_config['copy_creation_task'],
			agent=self.creative_content_creator(),
   		context=[self.marketing_strategy_task(), self.campaign_idea_task()],
			output_json=Copy,
			output_file=os.path.join(self.folder_path, "creative_creator_copy_creation.md")
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the MarketingPosts crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)

	def generate_master_report(self):
		"""Concatenates all agent reports into a master report"""
		master_report_path = os.path.join(self.folder_path, "master-report.md")
		
		# Find all markdown files in the folder
		md_files = glob.glob(os.path.join(self.folder_path, "*.md"))
		
		# Filter out the master report itself if it already exists
		md_files = [f for f in md_files if os.path.basename(f) != "master-report.md"]
		
		# Sort files to ensure deterministic order (e.g., by name)
		# Since our filenames are descriptive, sorting by name is reasonable,
		# or we could rely on task order if we tracked it, but name sort is safer for now.
		md_files.sort()
		
		with open(master_report_path, "w") as outfile:
			outfile.write(f"# Master Marketing Report: {self.output_name}\n")
			outfile.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
			
			for filepath in md_files:
				filename = os.path.basename(filepath)
				agent_task_name = filename.replace(".md", "").replace("_", " ").title()
				
				outfile.write(f"\n---\n## Report: {agent_task_name}\n---\n\n")
				
				try:
					with open(filepath, "r") as infile:
						outfile.write(infile.read())
						outfile.write("\n\n")
				except Exception as e:
					outfile.write(f"Error reading {filename}: {str(e)}\n")
					
		print(f"\n[Master Report] Generated at: {master_report_path}")
