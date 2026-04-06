# Attention Benchmark for AGI Evaluation

A benchmark submitted to the **Google DeepMind x Kaggle AGI Benchmark Hackathon** that evaluates language model attentional control across three cognitive tasks drawn from human neuropsychology. Rather than testing factual recall or reasoning in isolation, this benchmark probes whether a model can direct, sustain, and divide its attention, core faculties in AGI evaluation.

Each notebook runs across all 33 models available in the Kaggle environment and uses a fixed judge for consistent cross-model scoring.

> **Environment note:** The submission notebooks are designed to run inside the **Kaggle notebook environment**, where `kaggle-benchmarks` is pre-installed and `kbench.llm`, `kbench.judge_llm`, and `kbench.llms` are auto-configured via injected credentials. They cannot make live API calls outside that environment.

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

Assertion counts are standardized at 5 criteria per task row:

| Task | Assertions per row | Total per model | Notes |
|---|---|---|---|
| Selective Attention | 5 judge criteria | 15 | |
| Sustained Attention | 5 judge criteria + 1 regex hard-check | 18 | regex verifies the final numeric answer independently of the judge |
| Divided Attention | 5 judge criteria | 15 | |

---

## Results

Evaluated across 33 models in the Kaggle environment. Full per-model breakdowns are available in the `results/` CSVs and in the executed notebooks.

| Task | Models | Avg Pass Rate | Top Score | Bottom Score |
|---|---|---|---|---|
| Selective Attention | 33 | 95.2% | 100% (14 models) | 73.3% |
| Sustained Attention | 33 | 90.9% | 94.4% (24 models) | 33.3% |
| Divided Attention | 33 | 91.3% | 93.3% (27 models) | 66.7% |

**Key findings:**

- Selective attention is the strongest task overall — 14 of 33 models achieved a perfect score, and no model scored below 73.3%.
- No model scored 100% on sustained or divided attention, confirming these tasks impose a measurable ceiling even for frontier models.
- The performance hierarchy holds across all 33 models: selective > divided ≈ sustained. Distractor filtering is better-supported in current LLMs than sequential tracking or simultaneous stream-splitting.
- `gemma-3-1b` is a consistent outlier across all three tasks (73.3% / 33.3% / 66.7%), with a particularly steep drop on sustained attention. It is the smallest model in the set by a significant margin.
- `gemini-2.0-flash` underperforms its newer variants on selective (80%) and sustained (77.8%), while `gemini-2.0-flash-lite` scores 94.4% on sustained — suggesting architectural or training differences beyond generation alone.

---

## Tech Stack

| Tool | Role |
|---|---|
| `kaggle-benchmarks` | Task definition, LLM access via `kbench.llm`, assertion framework |
| `pandas` | TASK_DATA definition and results aggregation |
| `conda` | Environment management (Python 3.11) |

---

## Repo Structure

```
.
├── notebooks/
│   ├── selective_attention_benchmark.ipynb
│   ├── sustained_attention_benchmark.ipynb
│   └── divided_attention_benchmark.ipynb
├── results/
│   ├── selective_attention_results.csv
│   ├── sustained_attention_results.csv
│   └── divided_attention_results.csv
├── environment.yml
├── README.md
└── PROGRESS.md
```
