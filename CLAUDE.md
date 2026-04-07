# Kaggle-DeepMind-Benchmark

## Project Overview
An attention benchmark for the Google DeepMind x Kaggle AGI Benchmark Hackathon.
The benchmark evaluates frontier models across three attention tasks: selective,
sustained, and divided attention. Each task is implemented as a self-contained
Kaggle notebook using the kaggle-benchmarks framework.

## Stack
- Python 3.11, conda, pandas
- kaggle-benchmarks (task definition, LLM access, assertions)
- GitHub for version control

## Structure
- notebooks/ -- Kaggle benchmark notebooks (overview) and task notebooks (single-model)
- results/ -- CSV output from each benchmark run
