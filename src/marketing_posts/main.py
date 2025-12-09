import sys
import yaml
import argparse
from pathlib import Path
from marketing_posts.crew import MarketingPostsCrew

def run():
    parser = argparse.ArgumentParser(description="Run the Synnovai Marketing Generator.")
    parser.add_argument('file', nargs='?', help='Path to the company info YAML file')
    parser.add_argument('-m', '--model', default='gemini/gemini-pro-latest', help='Gemini model to use (e.g., gemini/gemini-1.5-pro, gemini/gemini-3-pro-preview)')
    
    args = parser.parse_args()

    # Check if a YAML file path is provided
    if args.file:
        try:
            with open(args.file, 'r') as f:
                inputs = yaml.safe_load(f)
            print(f"Loaded inputs from {args.file}")
        except FileNotFoundError:
            print(f"Error: File {args.file} not found.")
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
    
    print(f"Using model: {args.model}")
    
    output_name = Path(args.file).stem if args.file else 'marketing'
    
    try:
        MarketingPostsCrew(model_name=args.model, output_name=output_name).crew().kickoff(inputs=inputs)
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
            raise e


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
