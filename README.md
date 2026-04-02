# Attention Benchmark for AGI Evaluation

A benchmark submitted to the **Google DeepMind x Kaggle AGI Benchmark Hackathon** that evaluates language model attentional control across three cognitive tasks drawn from human neuropsychology. Rather than testing factual recall or reasoning in isolation, this benchmark probes whether a model can direct, sustain, and divide its attention — core faculties in AGI evaluation.

---

## Tasks

### Selective Attention
The model is given a passage with deliberately embedded distractors and must extract only goal-relevant information, ignoring content that co-occurs with but is irrelevant to the target question.

*Example:* A clinical note mixing vital signs with personal anecdotes. The model must report the clinical observations only.

### Sustained Attention
The model must track and aggregate specific targets accurately across a long sequential context — 14 to 15 records — without skipping entries, approximating, or losing count midway. A hard regex assertion checks the final answer; a judge LLM evaluates the reasoning.

*Example:* 15 financial transactions involving multiple parties. The model must calculate one person's exact net balance showing all working.

### Divided Attention
The model is given two independent named streams (`stream_a`, `stream_b`) and must simultaneously monitor and reason across both without conflating information between them.

*Example:* Log files from two servers running in parallel. The model must report error counts per server and identify which error type appeared on both.

---

## Results

Evaluated against the Kaggle-hosted model in the competition environment.

| Task | Assertions Passed | Pass Rate |
|---|---|---|
| Selective Attention | 14 / 14 | 100% |
| Sustained Attention | 19 / 20 | 95% |
| Divided Attention | 14 / 15 | 93% |

**Key finding:** The model performs perfectly on selective attention but degrades under sustained and divided attention demands — consistent with known limitations in long-horizon tracking and simultaneous multi-stream reasoning. This mirrors human attentional profiles and suggests filtering (selective) is better-supported in current LLMs than tracking (sustained) or splitting focus (divided).

---

## Tech Stack

| Tool | Role |
|---|---|
| `kaggle-benchmarks` | Task definition, LLM access via `kbench.llm`, assertion framework |
| `pandas` | TASK_DATA definition and results aggregation |
| `pytest` | Smoke tests for imports and data structure |
| `conda` | Environment management (Python 3.11) |
| `python-dotenv` | Local env var loading |

---

## Running Locally

**Install dependencies**
```bash
conda env create -f environment.yml
conda activate kaggle-deepmind
```

**Run smoke tests**
```bash
python -m pytest tests/test_pipeline.py -v
```

**Preview task data without making API calls**
```bash
python -m scripts.run_local
```

> Live model execution requires running inside the Kaggle notebook environment where `kbench.llm` is auto-configured via injected credentials.

---

## Repo Structure

```
.
├── notebooks/
│   ├── selective_attention_benchmark.ipynb  # Kaggle submission — selective attention
│   ├── sustained_attention_benchmark.ipynb  # Kaggle submission — sustained attention
│   └── divided_attention_benchmark.ipynb    # Kaggle submission — divided attention
├── src/
│   ├── tasks/
│   │   ├── selective_attention.py  # TASK_DATA + @kbench.task function
│   │   ├── sustained_attention.py  # TASK_DATA + @kbench.task function
│   │   └── divided_attention.py    # TASK_DATA + @kbench.task function
│   ├── evaluation/
│   │   └── runner.py               # Runs all tasks and logs results to CSV
│   └── utils/
│       └── config.py               # Shared path constants
├── scripts/
│   └── run_local.py                # Dry-run preview — no API calls
├── tests/
│   └── test_pipeline.py            # Smoke tests (4/4 passing)
├── results/                        # CSV output directory
└── environment.yml                 # Conda environment spec
```
