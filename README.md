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
| Selective Attention | 33 | 96.0% | 100% (18 models) | 66.7% |
| Sustained Attention | 33 | 97.5% | 100% (28 models) | 40.0% |
| Divided Attention | 33 | 92.6% | 100% (12 models) | 68.0% |

**Key findings:**

- Divided attention is the strongest discriminator: 8 distinct performance levels, a 32pp spread (100% to 68%), and only 12 of 33 models at a perfect score. It is the only task where a model's score meaningfully separates it from peers at the same capability tier.
- Selective attention is well-calibrated at 4 distinct levels (100% to 66.7%), with 18 of 33 models at a perfect score and 13 more at 93.3%. The spread is real but compressed near the top.
- Sustained attention exposes a ceiling effect: 28 of 33 models scored 100%, and the remaining 5 non-outlier models cluster between 90% and 97%. It is the most reliable identifier of small-model failure but contributes little differentiation among frontier models.
- Only 5 models scored 100% across all three tasks: `claude-opus-4-1`, `claude-sonnet-4-6`, `deepseek-v3.1`, `gemini-3.1-pro-preview`, and `qwen3-235b-a22b-instruct-2507`.
- Divided attention reveals capability gaps invisible in the other tasks. `gpt-oss-120b` (76%), `gpt-5.4-mini` (80%), `gemma-3-12b` (84%), and `gemini-2.5-flash` (84%) all score 100% on sustained and selective yet drop sharply on divided, suggesting a specific weakness in simultaneous multi-stream reasoning.
- `gemma-3-1b` is the consistent low outlier across all three tasks (66.7% / 40.0% / 68.0%). Its steepest drop is on sustained attention, where sequential numerical tracking under constraint is most demanding.
- `gemini-2.0-flash` scores 100% on both sustained and divided while scoring only 86.7% on selective, a rare pattern suggesting relative strength in structured multi-step tasks versus distractor filtering.
- Per-criterion analysis pinpoints the exact failure modes. In divided attention, halt cause attribution in the factory scenario drives the majority of failures: 15 of 33 models failed to correctly attribute Factory B's supply delay halt, and 14 of 33 failed Factory A's equipment calibration halt — the two highest individual criterion failure rates in the entire benchmark. Output and defect counts on the same scenario failed in only 2 and 1 models respectively, confirming the challenge is attribution under concurrent load, not arithmetic.
- In selective attention, 13 of 33 models failed a single criterion: not mentioning the lead researcher's hiking hobby in the research study scenario. This one distractor accounts for nearly all of selective attention's failures and reflects a specific model behavior — summarizing the full passage context rather than filtering to the task-relevant content.
- In sustained attention, the regex hard-check correctly identifies 4 models that gave wrong final numeric answers on the Alice net balance scenario (`claude-haiku`, `claude-opus-4-6`, `gpt-oss-20b`, and `gemma-3-1b`). These are the same models that appear below 100% in the summary results, confirming the hard-check is functioning as intended.

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
