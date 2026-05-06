# Solid State Electrolyte Analysis

This repository contains tools, scripts, and models for analyzing solid-state electrolytes, querying material properties, and predicting ionic conductivities using machine learning approaches.

## Repository Structure

- **`data/`**: Contains materials datasets (e.g., `all.csv`).
- **`models/`**: Stores trained machine learning models, such as the Random Forest model bundled in `rf_model_bundle.pkl`.
- **`scripts/`**: Python scripts for executing various tasks:
  - `obelix_query.py`: Script to query/interface with OBELiX or material databases.
  - `rf_predict.py`: Script to run predictions using the pre-trained Random Forest model.
- **`references/`**: Contains documentation, templates, and guidelines:
  - `example_materials.md`
  - `feishu_format.md`
  - `lessons_learned.md`
  - `model_details.md`
  - `mp_api_notes.md`
  - `report_template.md`
- **`SKILL.md`**: AI assistant/Agent skill definition files.

## Getting Started

### Prerequisites

Ensure you have Python environment set up with the required libraries to run the scripts in the `scripts/` directory.

### Usage

1. **Prediction**: You can use the prediction script to evaluate new materials.
   ```bash
   python scripts/rf_predict.py
   ```
2. **Data Querying**: Use the query script to fetch data.
   ```bash
   python scripts/obelix_query.py
   ```

## Notes

Documentation and implementation details can be found under the `references/` directory.
