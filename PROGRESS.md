# Project Progress

## Overview

This project is a submission for the **Google DeepMind x Kaggle AGI Benchmark Hackathon**. The goal is to design and implement a benchmark that evaluates a language model's attentional control (a cognitive faculty considered central to general intelligence). Rather than testing factual recall or reasoning in isolation, this benchmark probes whether a model can direct, sustain, and divide its attention the way a capable agent must when operating in noisy, multi-stream, or long-horizon environments.

The benchmark is implemented using the `kaggle-benchmarks` framework. The submission notebooks are designed to run inside the **Kaggle notebook environment**, where `kaggle-benchmarks` is pre-installed and `kbench.llm`, `kbench.judge_llm`, and `kbench.llms` are auto-configured via injected credentials. Each notebook evaluates all 33 available models using a fixed judge for consistent cross-model scoring.

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
| `conda` | Environment management (`kaggle-deepmind` env, Python 3.11) |
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
├── CLAUDE.md                                # Project context for Claude Code
├── PROGRESS.md                              # This file
└── environment.yml                          # Conda environment specification
```

---

## Key Technical Decisions

**Multi-model evaluation via `kbench.llms`**
Each notebook loops over all models available in the Kaggle environment (`kbench.llms`, 33 models) and runs every task row against each one. This turns each notebook into a comparative benchmark rather than a single-model pass/fail report, substantially increasing the signal.

**Fixed judge for cross-model comparability**
All responses are evaluated by a single fixed judge (`kbench.judge_llm`) rather than having each model grade its own output. This eliminates self-evaluation bias and ensures scores are directly comparable across models.

**`assess_response_with_judge` for nuanced evaluation**
Attention failures are rarely binary. A model might include some relevant information while still incorporating distractors. Using a judge LLM to evaluate criteria allows partial credit detection and natural-language criteria that would be impossible to capture with regex or exact match.

**Dual assertion strategy in sustained attention**
Sustained attention tasks use both `assert_contains_regex` (hard check on the final numeric answer) and `assess_response_with_judge` (soft check on the reasoning steps). This separates correctness of the final answer from correctness of the tracking process, giving a richer signal than either check alone.

**Standardized assertion counts**
All tasks use 5 judge-evaluated criteria per row (15 total for selective and divided). Sustained attention adds 1 regex hard-check per row (18 total), which is intentional: the regex verifies the final numeric answer independently of the judge, serving a structurally different purpose.

**Two-stream design for divided attention**
Passing two named streams as distinct parameters (rather than interleaved text) makes the task structure explicit in the prompt and ensures the model cannot treat the input as a single unified context. This cleanly isolates the divided attention challenge from general reading comprehension.

**One notebook per task as submission artifact**
The benchmark is split into three self-contained notebooks, one per task. This matches the hackathon's submission format, keeps each notebook focused and independently runnable, and ensures all of `kbench.llm`, `kbench.judge_llm`, and `kbench.llms` are auto-configured by the Kaggle environment without any local setup.

---

## Benchmark Results

Each notebook evaluates 33 models. Results vary by model; the summary table produced by each notebook ranks models by pass rate for that task. Sustained attention assertions total 18 per model (5 criteria + 1 regex per row); selective and divided total 15 per model.

Initial single-model results (prior to multi-model update, against the Kaggle default model):

| Task | Assertions Passed | Pass Rate | Notes |
|---|---|---|---|
| Selective Attention | 14 / 15 | 93% | One distractor criterion added in standardization pass |
| Sustained Attention | 18 / 18 | 100% | Criteria trimmed from 20 to 18 in standardization pass |
| Divided Attention | 14 / 15 | 93% | One stream conflation in the portfolio row |

Multi-model results pending re-run of all three updated notebooks in Kaggle.

---

## Current Status

**Notebooks updated. Ready for re-submission.**

All three notebooks have been updated to the multi-model evaluation design. Pending re-run in the Kaggle environment to collect cross-model results.

---

## Retrospective Notes

- Arithmetic errors in sustained attention data were caught only during live execution, not during local testing. A local dry-run mode that validates expected answers against deterministic inputs would have caught these earlier.
- The `assess_response_with_judge` results must be explicitly registered via an `assert_true` loop to appear in `run.assertion_results`. This is not obvious from the kbench documentation and was discovered through live debugging.
- Splitting into three notebooks (rather than one combined notebook) simplified the submission process and made each task independently reviewable by judges.
