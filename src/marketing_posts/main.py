#!/usr/bin/env python
import sys
import yaml
from marketing_posts.crew import MarketingPostsCrew

def run():
    # Check if a YAML file path is provided
    if len(sys.argv) > 1 and sys.argv[1].endswith('.yaml'):
        try:
            with open(sys.argv[1], 'r') as f:
                inputs = yaml.safe_load(f)
            print(f"Loaded inputs from {sys.argv[1]}")
        except FileNotFoundError:
            print(f"Error: File {sys.argv[1]} not found.")
            sys.exit(1)
        except yaml.YAMLError as exc:
            print(f"Error parsing YAML file: {exc}")
            sys.exit(1)
    else:
        # Default inputs
        print("No YAML file provided, using default inputs.")
        inputs = {
            'customer_domain': 'crewai.com',
            'project_description': """
CrewAI, a leading provider of multi-agent systems, aims to revolutionize marketing automation for its enterprise clients. This project involves developing an innovative marketing strategy to showcase CrewAI's advanced AI-driven solutions, emphasizing ease of use, scalability, and integration capabilities. The campaign will target tech-savvy decision-makers in medium to large enterprises, highlighting success stories and the transformative potential of CrewAI's platform.

Customer Domain: AI and Automation Solutions
Project Overview: Creating a comprehensive marketing campaign to boost awareness and adoption of CrewAI's services among enterprise clients.
"""
        }
    
    MarketingPostsCrew().crew().kickoff(inputs=inputs)


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
        MarketingPostsCrew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
