# Synnovai Marketing Generator

This project leverages the **CrewAI** framework and **Google Gemini** models to automate the creation of comprehensive marketing strategies. It orchestrates a team of autonomous AI agents—a Lead Market Analyst, a Chief Marketing Strategist, and a Creative Content Creator—to research, plan, and generate marketing content.

## Features

- **Google Gemini Integration**: Uses `gemini-pro-latest` by default, with support for all Gemini models (Flash, Pro, Exp, etc.).
- **Dynamic Inputs**: Accepts company information via easy-to-edit YAML files.
- **Robust Output Management**:
    - **Timestamped Folders**: Every run creates a unique folder under `Reports/` (e.g., `Reports/20241209_153000_tjsammtg/`).
    - **Individual Reports**: Each agent's work is saved to a distinct markdown file within that folder.
    - **Master Report**: A single `master-report.md` concatenates all outputs into one final document.
    - **Clean Repo**: generated reports are automatically git-ignored.
- **Smart Error Handling**: Includes a custom JSON linter that automatically repairs malformed LLM outputs and provides clear error messages if validation fails.
- **CLI Support**: Full command-line interface for file selection and model switching.

## Prerequisites

- Python 3.10 - 3.13
- [Google Gemini API Key](https://aistudio.google.com/)
- [Serper API Key](https://serper.dev/) (for Google Search capabilities)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd synnovai_marketing_generator
    ```

2.  **Set up the environment:**
    Create a `.env` file in the root directory:
    ```env
    GEMINI_API_KEY=your_gemini_api_key_here
    SERPER_API_KEY=your_serper_api_key_here
    ```

3.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -e .
    ```

## Usage

### Basic Run
Run the generator with a company information YAML file:
```bash
marketing_posts company_info.yaml
```

### View Available Models
List all compatible Gemini models available to your API key:
```bash
marketing_posts -h
```

### Select a Specific Model
Use the `--model` flag to experiment with different Gemini versions (e.g., faster Flash models or experimental builds):
```bash
marketing_posts company_info.yaml --model gemini/gemini-2.0-flash
```

## Input Format (YAML)

Create a YAML file (e.g., `my_company.yaml`) with the following structure:

```yaml
name: "Synnovai"
website: "https://synnovai.com"
customer_domain: "synnovai.com"
description: "Synnovai is an AI-powered marketing agency..."
# gem_url: "https://gemini.google.com/share/..." (Optional: URL for agent context)
```

## Output Structure

After a successful run, you will find a new folder in `Reports/`:

```text
Reports/
└── 20241209_141000_synnovai/
    ├── lead_market_analyst_research.md
    ├── chief_strategist_project_understanding.md
    ├── chief_strategist_marketing_strategy.md
    ├── creative_creator_campaign_ideas.md
    ├── creative_creator_copy_creation.md
    └── master-report.md
```

## License
MIT License
