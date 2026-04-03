# Kaggle-DeepMind-Benchmark

## Project Overview
An attention benchmark for the Google DeepMind x Kaggle AGI Benchmark Hackathon.
The benchmark evaluates frontier models across three attention tasks: selective,
sustained, and divided attention. Each task is implemented as a self-contained
Kaggle notebook using the kaggle-benchmarks framework.

## Stack
- Python 3.11, conda, pandas, pytest
- kaggle-benchmarks (task definition, LLM access, assertions)
- GitHub for version control

## Structure
- src/tasks/ — task definitions (TASK_DATA and @kbench.task functions)
- notebooks/ — Kaggle submission notebooks, one per task
- scripts/ — local dry-run tooling, no API calls
- tests/ — smoke tests for import integrity and data structure
- results/ — CSV output directory
