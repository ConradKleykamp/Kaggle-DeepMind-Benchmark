# Kaggle-DeepMind-Benchmark

## Project Overview
Building an attention benchmark for the Google DeepMind x Kaggle AGI 
hackathon. The benchmark evaluates frontier models across three attention 
tasks: selective, sustained, and divided attention.

## Stack
- Python, conda, pandas, MLflow, pytest
- Anthropic/OpenAI SDKs for model evaluation
- GitHub for version control

## Standing Instructions
After completing any meaningful unit of work, update PROGRESS.md with:
- What was built or changed
- Key decisions made and why
- Current project status
- Immediate next steps

Keep PROGRESS.md current at all times. It is the single source of truth 
for project progress and will form the basis of the final competition writeup.

## Structure
- src/tasks/ — attention task generators
- src/evaluation/ — scoring and model evaluation
- src/utils/ — shared helpers
- data/raw/ and data/processed/ — data layers
- notebooks/ — EDA and prototyping
- results/ — model outputs and scores