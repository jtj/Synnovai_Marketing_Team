import sys
import yaml
import argparse
from pathlib import Path
from marketing_posts.crew import MarketingPostsCrew
from marketing_posts.knowledge_loader import KnowledgeLoader

def run():
    model_list = """
Available Models (Partial List):
  - gemini/gemini-pro-latest (Default)
  - gemini/gemini-flash-latest
  - gemini/gemini-2.0-flash
  - gemini/gemini-2.0-flash-exp
  - gemini/gemini-2.0-flash-lite-preview-02-05
  - gemini/gemini-2.0-pro-exp-02-05
  - gemini/gemini-2.5-flash
  - gemini/gemini-3-pro-preview
  - gemini/gemini-exp-1206
  - gemini/gemini-1.5-pro-latest
  - gemini/gemini-1.5-flash-latest

(Note: You can use any model available to your API key, prefixed with 'gemini/')
"""
    parser = argparse.ArgumentParser(
        description="Run the Synnovai Marketing Generator.",
        epilog=model_list,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('file', nargs='?', help='Path to the company info YAML file')
    parser.add_argument('-m', '--model', default='gemini/gemini-pro-latest', help='Gemini model to use. See below for options.')

    
    args = parser.parse_args()

    # Check if a YAML file path is provided
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            # Check in companies/ directory
            companies_path = Path("companies") / args.file
            if companies_path.exists():
                file_path = companies_path
            else:
                 print(f"Error: File {args.file} not found locally or in companies/ directory.")
                 sys.exit(1)

        try:
            with open(file_path, 'r') as f:
                inputs = yaml.safe_load(f)
            print(f"Loaded inputs from {file_path}")
        except yaml.YAMLError as exc:
            print(f"Error parsing YAML file: {exc}")
            sys.exit(1)
            
        # Optional Gem URL input
        # Optional Gem URL input (Legacy support, but we don't use it for scraping anymore if prohibited)
        if 'gem_url' not in inputs:
            inputs['gem_url'] = "No additional URL provided."
        
        # Load Company Knowledge from Folder
        company_knowledge_content = ""
        
        # Determine company name from inputs
        company_name = inputs.get('name')
        if company_name:
            folder_knowledge = KnowledgeLoader.load_knowledge(company_name)
            if folder_knowledge:
                company_knowledge_content += folder_knowledge
                print(f"Loaded company knowledge from folder '{company_name}'")
        else:
             print("Warning: 'name' field not found in YAML. Cannot load company folder.")

        if company_knowledge_content:
            inputs['company_knowledge'] = company_knowledge_content
        else:
            inputs['company_knowledge'] = "No local company knowledge found."
            
    else:
        # Default inputs
        print("No YAML file provided, using default inputs.")
        inputs = {
            'customer_domain': 'crewai.com',
            'project_description': """
CrewAI, a leading provider of multi-agent systems, aims to revolutionize marketing automation for its enterprise clients. This project involves developing an innovative marketing strategy to showcase CrewAI's advanced AI-driven solutions, emphasizing ease of use, scalability, and integration capabilities. The campaign will target tech-savvy decision-makers in medium to large enterprises, highlighting success stories and the transformative potential of CrewAI's platform.

Customer Domain: AI and Automation Solutions
Project Overview: Creating a comprehensive marketing campaign to boost awareness and adoption of CrewAI's services among enterprise clients.
""",
            'gem_url': "No additional URL provided.",
            'company_knowledge': "No local company knowledge found."
        }
    
    print(f"Using model: {args.model}")
    
    output_name = Path(args.file).stem if args.file else 'marketing'
    
    crew_instance = None
    try:
        crew_instance = MarketingPostsCrew(model_name=args.model, output_name=output_name)
        crew_instance.crew().kickoff(inputs=inputs)
    except Exception as e:
        # Check if it looks like a JSON validation error
        if "Invalid JSON" in str(e) or "pydantic" in str(e).lower():
            print("\n" * 2)
            print("JJJJJ   SSSS   OOO   N   N      FFFFF   AAA   IIIII  L")
            print("  J    S      O   O  NN  N      F      A   A    I    L")
            print("  J     SSSS  O   O  N N N      FFF    AAAAA    I    L")
            print("J J        S  O   O  N  NN      F      A   A    I    L")
            print(" J     SSSS    OOO   N   N      F      A   A  IIIII  LLLLL")
            print("\n" * 2)
            print(f"Detailed Error: {e}")
        else:
            print(f"An error occurred: {e}")
            # We don't raise here if we want the finally block to run and then perhaps exit gracefully,
            # but raising is fine too; finally will still run.
            # Let's re-raise to be safe and show full traceback if needed, 
            # but usually for a user app printing the error is cleaner.
            # For now, let's just print.
    finally:
        if crew_instance:
            print("\nGenerating Master Report...")
            crew_instance.generate_master_report()


def train():
    """
    Train the crew for a given number of iterations.
    """
    # ... (Train logic remains mostly same, or could also accept YAML but sticking to scope for now)
    inputs = {
        'customer_domain': 'crewai.com',
        'project_description': """
CrewAI, a leading provider of multi-agent systems, aims to revolutionize marketing automation for its enterprise clients. This project involves developing an innovative marketing strategy to showcase CrewAI's advanced AI-driven solutions, emphasizing ease of use, scalability, and integration capabilities. The campaign will target tech-savvy decision-makers in medium to large enterprises, highlighting success stories and the transformative potential of CrewAI's platform.

Customer Domain: AI and Automation Solutions
Project Overview: Creating a comprehensive marketing campaign to boost awareness and adoption of CrewAI's services among enterprise clients.
"""
    }
    try:
        # Pass default model for training or add CLI args here too if needed
        MarketingPostsCrew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
