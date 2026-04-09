# Attention Benchmark for AGI Evaluation

A benchmark submitted to the **Google DeepMind x Kaggle AGI Benchmark Hackathon** that evaluates language model attentional control across three cognitive tasks drawn from human neuropsychology. Rather than testing factual recall or reasoning in isolation, this benchmark probes whether a model can direct, sustain, and divide its attention, core faculties in AGI evaluation.

The benchmark notebooks run across all 33 models available in the Kaggle environment and use a fixed judge for consistent cross-model scoring. Task notebooks are also included for single-model evaluation via the Kaggle task runner.

> **Environment note:** The submission notebooks are designed to run inside the **Kaggle notebook environment**, where `kaggle-benchmarks` is pre-installed and `kbench.llm`, `kbench.judge_llm`, and `kbench.llms` are auto-configured via injected credentials. They cannot make live API calls outside that environment.

> **LLM Usage:** Claude Code was used throughout this project as a development assistant, primarily for code tuning, implementation debugging, and refining task criteria wording. Task design, scenario selection, and all analytical judgements are my own.

---

## Tasks

### Selective Attention
The model is given a passage with deliberately embedded distractors and must extract only goal-relevant information, ignoring content that is irrelevant to the target question.

*Example:* A clinical note mixing vital signs with personal anecdotes. The model must report the clinical observations only.

### Sustained Attention
The model must track and aggregate specific targets accurately across a sequential context of up to 15 records, without skipping entries, approximating, or losing count midway.

*Example:* 15 financial transactions involving multiple parties. The model must calculate one person's exact net balance, showing all working.

### Divided Attention
The model is given two independent information streams and must simultaneously monitor and reason across both, keeping each stream's facts correctly attributed without conflation.

*Example:* Log files from two servers running in parallel. The model must report error counts per server and identify which error type appeared on both.

---

## Evaluation Design

Each notebook runs across all models available in the Kaggle environment (`kbench.llms`, 33 models evaluated) using a fixed judge model (`kbench.judge_llm`) to score every response. Using a fixed judge rather than self-evaluation eliminates the bias of each model grading its own output, making scores directly comparable across models.

Each task uses 5 judge-evaluated criteria per scenario. Scenario counts differ across tasks because each was calibrated to the configuration that maximized performance discrimination: additional scenarios improved spread for sustained and divided attention but compressed it for selective attention. Pass rates are used for all cross-task comparisons.

| Task | Scenarios | Assertions per scenario | Total per model | Notes |
|---|---|---|---|---|
| Selective Attention | 3 | 5 judge criteria | 15 | |
| Sustained Attention | 5 | 5 judge criteria + 1 regex hard-check | 30 | regex verifies the final numeric answer independently of the judge |
| Divided Attention | 5 | 5 judge criteria | 25 | |

---

## Results

Evaluated across 33 models in the Kaggle environment. Full per-model breakdowns are available in the `results/` CSVs and in the executed notebooks.

> **Note:** LLM outputs are non-deterministic and no random seed can be set for hosted models. Pass rates may vary slightly across runs. The figures below reflect a single full evaluation run.

| Task | Models | Avg Pass Rate | Top Score | Bottom Score |
|---|---|---|---|---|
| Selective Attention | 33 | 95.2% | 100% (14 models) | 73.3% |
| Sustained Attention | 33 | 96.8% | 100% (25 models) | 36.7% |
| Divided Attention | 33 | 93.6% | 100% (16 models) | 68.0% |

**Key findings:**

- Divided attention is the most discriminating task: 7 distinct performance levels, a 32pp spread (100% to 68%), and only 16 of 33 models at a perfect score. Multi-stream reasoning with numerical content is the hardest attentional demand tested.
- Selective attention shows a consistent spread: 14 of 33 models scored 100% and no model scored below 73.3%, with a 26.7pp range driven largely by smaller models.
- Sustained attention has the highest average (96.8%) but a bimodal distribution: 25 of 33 models scored 100%, while the remaining 8 spread between 90% and 36.7%. The task is well-handled by most frontier models but exposes significant weaknesses in smaller ones.
- `gemma-3-1b` is a consistent low outlier across all three tasks (73.3% / 36.7% / 68.0%), with a particularly steep drop on sustained attention. It is the smallest model in the evaluated set by a significant margin.
- `gemini-2.0-flash` underperforms its generation on selective (80%) and scores below the median on divided (92%), while `gemini-2.0-flash-lite` scores 100% on sustained, suggesting training differences that do not track model size or generation number alone.
- Per-row analysis in the executed notebooks indicates that failures in divided attention cluster in scenarios requiring simultaneous numerical reasoning across both streams, while simpler stream-identification scenarios show near-universal pass rates.

---

## Tech Stack

| Tool | Role |
|---|---|
| `kaggle-benchmarks` | Task definition, LLM access via `kbench.llm`, assertion framework |
| `pandas` | TASK_DATA definition and results aggregation |

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
├── README.md
└── PROGRESS.md
```
