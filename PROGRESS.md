# Project Progress

## Overview

This project is a submission for the **Google DeepMind x Kaggle AGI Benchmark Hackathon**. The goal is to design and implement a benchmark that evaluates a language model's attentional control — a cognitive faculty considered central to general intelligence. Rather than testing factual recall or reasoning in isolation, this benchmark probes whether a model can direct, sustain, and divide its attention the way a capable agent must when operating in noisy, multi-stream, or long-horizon environments.

The benchmark is implemented using the `kaggle-benchmarks` framework and is designed to run as a Kaggle notebook where model access and credentials are auto-configured.

---

## Three Attention Tasks

- **Selective Attention** — The model must extract goal-relevant information from a passage containing deliberately embedded distractors, ignoring irrelevant content that co-occurs with target information.
- **Sustained Attention** — The model must track and aggregate specific targets accurately across a long sequential context, without skipping entries, approximating, or losing count midway.
- **Divided Attention** — The model must simultaneously monitor and reason across two independent information streams, keeping each stream's facts correctly attributed without conflation.

---

## Tech Stack

| Tool | Role |
|---|---|
| `kaggle-benchmarks` | Task definition, LLM access, assertion framework, `Run` result tracking |
| `pandas` | TASK_DATA definition, results aggregation into DataFrame |
| `pytest` | Smoke tests for import integrity and data structure validation |
| `conda` | Environment management (`kaggle-deepmind` env, Python 3.11) |
| `python-dotenv` | Local env var loading (not used in Kaggle; env is auto-injected) |
| GitHub | Version control and remote backup |
| Claude Code | Development assistant throughout — architecture, implementation, debugging |
| VS Code | Primary editor with Jupyter notebook support |

---

## File Structure

```
.
├── notebooks/
│   ├── selective_attention_benchmark.ipynb  # Kaggle submission — selective attention task
│   ├── sustained_attention_benchmark.ipynb  # Kaggle submission — sustained attention task
│   ├── divided_attention_benchmark.ipynb    # Kaggle submission — divided attention task
│   └── attention_benchmark.ipynb            # Original combined notebook (superseded)
├── src/
│   ├── tasks/
│   │   ├── selective_attention.py  # TASK_DATA + @kbench.task for selective attention
│   │   ├── sustained_attention.py  # TASK_DATA + @kbench.task for sustained attention
│   │   └── divided_attention.py    # TASK_DATA + @kbench.task for divided attention
│   ├── evaluation/
│   │   └── runner.py               # Ties all three tasks together; logs results to CSV
│   └── utils/
│       └── config.py               # Loads .env; exports RESULTS_DIR and shared path constants
├── scripts/
│   └── run_local.py                # Local dry-run tool — previews all task rows without API calls
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
Attention failures are rarely binary — a model might include some relevant information while still incorporating distractors. Using a judge LLM to evaluate criteria allows partial credit detection and natural-language criteria (e.g. "response does not dwell on researcher hobbies") that would be impossible to capture with regex or exact match.

**`assert_true` loop for registering judge results**
`assess_response_with_judge` returns a report object; its results are not automatically registered as assertions on the `Run`. Iterating `report.results` and calling `kbench.assertions.assert_true(result.passed, expectation=result.criterion)` for each criterion ensures every judgment is individually tracked in `run.assertion_results` and visible in the results DataFrame.

**Dual assertion strategy in sustained attention**
Sustained attention tasks use both `assert_contains_regex` (hard check on the final numeric answer) and `assess_response_with_judge` (soft check on the reasoning steps). This separates correctness of the final answer from correctness of the tracking process, giving a richer signal than either check alone.

**Format-flexible regex patterns in sustained attention**
`assert_contains_regex` patterns account for number formatting variants the model might produce: `-225` vs `negative $225` (row 0), and `21391` vs `$21,391` (row 2). This prevents false negatives from formatting differences rather than reasoning failures.

**Two-stream design for divided attention**
Passing two named streams (`stream_a`, `stream_b`) as distinct parameters — rather than interleaved text — makes the task structure explicit in the prompt and ensures the model cannot treat the input as a single unified context. This cleanly isolates the divided attention challenge from general reading comprehension.

**One notebook per task as submission artifact**
The benchmark is split into three self-contained notebooks, one per task. This matches the hackathon's one-task-per-notebook submission format, keeps each notebook focused and independently runnable, and ensures `kbench.llm` is auto-configured by the Kaggle environment without any local setup.

**Arithmetic corrections in sustained attention**
Two data errors were caught via live execution and corrected: Row 0 (Alice net balance: `-200 + 300 - 75 - 250 = -225`, not `-75`) and Row 2 (electronics inventory total: `4186 + 5394 + 5970 + 5841 = $21391`, not `$18212`). Both `expected_answer` and the corresponding criterion strings were updated across the `.py` source file and all notebooks.

---

## Benchmark Results

Evaluated against the Kaggle-hosted model in the competition notebook environment.

| Task | Assertions Passed | Pass Rate | Notes |
|---|---|---|---|
| Selective Attention | 14 / 14 | 100% | Perfect distractor filtering across all 3 rows |
| Sustained Attention | 19 / 20 | 95% | One miss on inventory calculation detail |
| Divided Attention | 14 / 15 | 93% | One stream conflation in the portfolio row |

**Key finding:** The model performs perfectly on selective attention but degrades measurably under sustained and divided attention demands — consistent with known limitations in long-horizon tracking and simultaneous multi-stream reasoning. This pattern mirrors human attentional profiles and suggests selective attention (filtering) is better-supported in current LLMs than sustained or divided attention (tracking and splitting focus).

---

## Current Status

**Complete. Submitted to Kaggle.**

All three task notebooks ran successfully in the Kaggle environment. Results recorded above. Smoke tests pass (4/4).

---

## Next Steps

- Monitor competition results and leaderboard position
- Consider extending with additional rows per task for more statistical power
- Explore whether prompt engineering (e.g. explicit chain-of-thought instructions) improves sustained and divided attention scores
