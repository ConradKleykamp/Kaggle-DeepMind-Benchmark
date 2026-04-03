# Project Progress

## Overview

This project is a submission for the **Google DeepMind x Kaggle AGI Benchmark Hackathon**. The goal is to design and implement a benchmark that evaluates a language model's attentional control (a cognitive faculty considered central to general intelligence). Rather than testing factual recall or reasoning in isolation, this benchmark probes whether a model can direct, sustain, and divide its attention the way a capable agent must when operating in noisy, multi-stream, or long-horizon environments.

The benchmark is implemented using the `kaggle-benchmarks` framework. The submission notebooks are designed to run inside the **Kaggle notebook environment**, where `kaggle-benchmarks` is pre-installed and the model (`kbench.llm`) is auto-configured via injected credentials.

---

## Three Attention Tasks

- **Selective Attention:** The model must extract goal-relevant information from a passage containing deliberately embedded distractors, ignoring irrelevant content that co-occurs with target information.
- **Sustained Attention:** The model must track and aggregate specific targets accurately across a long sequential context, without skipping entries, approximating, or losing count midway.
- **Divided Attention:** The model must simultaneously monitor and reason across two independent information streams, keeping each stream's facts correctly attributed without conflation.

---

## Tech Stack

| Tool | Role |
|---|---|
| `kaggle-benchmarks` | Task definition, LLM access, assertion framework, `Run` result tracking |
| `pandas` | TASK_DATA definition, results aggregation into DataFrame |
| `pytest` | Smoke tests for import integrity and data structure validation |
| `conda` | Environment management (`kaggle-deepmind` env, Python 3.11) |
| `python-dotenv` | Local env var loading (not used in Kaggle, env is auto-injected) |
| GitHub | Version control and remote backup |
| Claude Code | Development assistant throughout (architecture, implementation, debugging) |
| VS Code | Primary editor with Jupyter notebook support |

---

## File Structure

```
.
├── notebooks/
│   ├── selective_attention_benchmark.ipynb  # Kaggle submission, selective attention task
│   ├── sustained_attention_benchmark.ipynb  # Kaggle submission, sustained attention task
│   └── divided_attention_benchmark.ipynb    # Kaggle submission, divided attention task
├── src/
│   ├── tasks/
│   │   ├── selective_attention.py  # TASK_DATA and @kbench.task for selective attention
│   │   ├── sustained_attention.py  # TASK_DATA and @kbench.task for sustained attention
│   │   └── divided_attention.py    # TASK_DATA and @kbench.task for divided attention
│   ├── evaluation/
│   │   └── runner.py               # Ties all three tasks together, logs results to CSV
│   └── utils/
│       └── config.py               # Loads .env, exports RESULTS_DIR and shared path constants
├── scripts/
│   └── run_local.py                # Local dry-run tool, previews all task rows without API calls
├── tests/
│   └── test_pipeline.py            # Smoke tests: validates TASK_DATA structure and runner imports
├── results/                        # Output directory for CSV results from runner.py
├── data/                           # Raw and processed data directories (reserved)
├── CLAUDE.md                       # Project context for Claude Code
├── PROGRESS.md                     # This file
└── environment.yml                 # Conda environment specification
```

---

## Key Technical Decisions

**`assess_response_with_judge` for nuanced evaluation**
Attention failures are rarely binary. A model might include some relevant information while still incorporating distractors. Using a judge LLM to evaluate criteria allows partial credit detection and natural-language criteria that would be impossible to capture with regex or exact match.

**Dual assertion strategy in sustained attention**
Sustained attention tasks use both `assert_contains_regex` (hard check on the final numeric answer) and `assess_response_with_judge` (soft check on the reasoning steps). This separates correctness of the final answer from correctness of the tracking process, giving a richer signal than either check alone. Regex patterns are format-flexible to avoid false negatives from comma or currency formatting variants.

**Two-stream design for divided attention**
Passing two named streams as distinct parameters (rather than interleaved text) makes the task structure explicit in the prompt and ensures the model cannot treat the input as a single unified context. This cleanly isolates the divided attention challenge from general reading comprehension.

**One notebook per task as submission artifact**
The benchmark is split into three self-contained notebooks, one per task. This matches the hackathon's submission format, keeps each notebook focused and independently runnable, and ensures `kbench.llm` is auto-configured by the Kaggle environment without any local setup.

---

## Benchmark Results

Evaluated against the Kaggle-hosted model in the competition notebook environment.

| Task | Assertions Passed | Pass Rate | Notes |
|---|---|---|---|
| Selective Attention | 14 / 14 | 100% | Perfect distractor filtering across all 3 rows |
| Sustained Attention | 19 / 20 | 95% | One miss on inventory calculation detail |
| Divided Attention | 14 / 15 | 93% | One stream conflation in the portfolio row |

The model performs perfectly on selective attention but degrades measurably under sustained and divided attention demands, consistent with known limitations in long-horizon tracking and simultaneous multi-stream reasoning. This pattern mirrors human attentional profiles and suggests selective attention (filtering) is better-supported in current LLMs than sustained or divided attention (tracking and splitting focus).

---

## Current Status

**Complete. Submitted to Kaggle.**

All three task notebooks ran successfully in the Kaggle environment. Results recorded above. Smoke tests pass (4/4).

---

## Retrospective Notes

- Arithmetic errors in sustained attention data were caught only during live execution, not during local testing. A local dry-run mode that validates expected answers against deterministic inputs would have caught these earlier.
- The `assess_response_with_judge` results must be explicitly registered via an `assert_true` loop to appear in `run.assertion_results`. This is not obvious from the kbench documentation and was discovered through live debugging.
- Splitting into three notebooks (rather than one combined notebook) simplified the submission process and made each task independently reviewable by judges.
