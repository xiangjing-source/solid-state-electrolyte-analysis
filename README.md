# Solid State Electrolyte Analysis (OpenClaw Skill)

This repository provides a packaged **Skill Integration for OpenClaw**, designed to empower agents with the capabilities to analyze solid-state electrolytes, query material properties, and predict ionic conductivities using machine learning approaches. 

By utilizing the encapsulated `SKILL.md` and associated scripts, OpenClaw agents can autonomously perform advanced material informatics workflows.

## Skill Features
- **Data Querying**: Automated interface with material databases and OBELiX frameworks mapping.
- **Property Prediction**: Pre-trained machine learning bundle (Random Forest inference) for evaluating novel solid-state materials' ionic conductivity.
- **Standardized Reporting**: Automatically formats outputs matching the expected Feishu / document templates.

## Repository Structure

- **`SKILL.md`**: The core OpenClaw skill definition file defining the prompts, execution context, and instructions for the agent.
- **`data/`**: Ground truth datasets and cached material properties (e.g., `all.csv`).
- **`models/`**: Stored machine learning models (`rf_model_bundle.pkl`) for offline inference.
- **`scripts/`**: Executable scripts invoked by the OpenClaw skill agent:
  - `obelix_query.py`: Interfaces with OBELiX/databases to fetch materials data.
  - `rf_predict.py`: Runs predictions using the bundled RF model.
- **`references/`**: Guidelines, documentation, and agent templates (`report_template.md`, `feishu_format.md`, `mp_api_notes.md`).

## Integration with OpenClaw

To use this skill within OpenClaw:
1. Ensure the Python environment specified by the project is installed and activated.
2. Load the `SKILL.md` file into your OpenClaw agent context or skill registry.
3. The agent will autonomously read the references, load the models, and execute the scripts (`scripts/rf_predict.py`, `scripts/obelix_query.py`) when relevant solid-state electrolyte tasks are requested.

## Prerequisites

Required dependencies for the sub-scripts should be installed via standard Python package managers in your target environment.
