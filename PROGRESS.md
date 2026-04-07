# Project Progress

## Overview

Submission for the **Google DeepMind x Kaggle AGI Benchmark Hackathon**. The benchmark evaluates language model attentional control across three cognitive tasks drawn from human neuropsychology, using the `kaggle-benchmarks` framework inside the Kaggle notebook environment.

---

## Status: Complete

All three tasks are implemented, executed, and submitted. Results have been collected across 33 models and are documented in the `results/` CSVs and executed benchmark notebooks.

---

## Tasks

- **Selective Attention:** Extract goal-relevant information from a passage containing deliberately embedded distractors.
- **Sustained Attention:** Track and aggregate specific targets accurately across a long sequential context without skipping entries or approximating.
- **Divided Attention:** Simultaneously monitor and reason across two independent information streams, keeping each stream's facts correctly attributed.

---

## Repo Structure

```
.
├── notebooks/
│   ├── divided_attention_benchmark.ipynb   # overview: runs all 33 models, visual output
│   ├── divided_attention_task.ipynb        # task runner: single model via kbench.llm
│   ├── selective_attention_benchmark.ipynb # overview: runs all 33 models, visual output
│   ├── selective_attention_task.ipynb      # task runner: single model via kbench.llm
│   ├── sustained_attention_benchmark.ipynb # overview: runs all 33 models, visual output
│   └── sustained_attention_task.ipynb      # task runner: single model via kbench.llm
├── results/
│   ├── divided_attention_results.csv
│   ├── selective_attention_results.csv
│   └── sustained_attention_results.csv
├── CLAUDE.md
├── PROGRESS.md
└── README.md
```

---

## Key Technical Decisions

**Multi-model evaluation via `kbench.llms`**
Each benchmark notebook loops over all 33 models available in the Kaggle environment and runs every task row against each one, producing a comparative benchmark rather than a single-model result.

**Fixed judge for cross-model comparability**
All responses are evaluated by a single fixed judge (`kbench.judge_llm`) rather than having each model grade its own output. This eliminates self-evaluation bias and keeps scores directly comparable across models.

**Task notebooks for single-model evaluation**
A second set of notebooks (`*_task.ipynb`) uses `kbench.llm` to run against a single injected model. These are compatible with the Kaggle task runner and support the "Run on new model" workflow on the task page.

**Dual assertion strategy in sustained attention**
Sustained attention uses both `assert_contains_regex` (hard check on the final numeric answer) and `assess_response_with_judge` (soft check on reasoning steps), separating correctness of the answer from correctness of the tracking process.

**Standardized assertion counts**
Selective and divided attention: 5 judge criteria per row, 15 total. Sustained attention: 5 judge criteria + 1 regex hard-check per row, 18 total.

---

## Results Summary

Evaluated across 33 models. Full breakdowns in `results/` CSVs.

| Task | Avg Pass Rate | Top Score | Bottom Score |
|---|---|---|---|
| Selective Attention | 95.2% | 100% (14 models) | 73.3% |
| Sustained Attention | 90.9% | 94.4% (24 models) | 33.3% |
| Divided Attention | 91.3% | 93.3% (27 models) | 66.7% |

`gemma-3-1b` is a consistent low outlier across all three tasks, and the only model to score below 80% on selective attention.

---

## Retrospective Notes

- The `assess_response_with_judge` results must be explicitly registered via an `assert_true` loop to appear in assertion results. This is not obvious from the documentation and was discovered through live debugging.
- Splitting into three notebooks simplified submission and made each task independently reviewable.
- Task notebooks were added after initial submission to support single-model evaluation via the Kaggle task runner.
