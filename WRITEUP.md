# Can AI Models Pay Attention?

**Subtitle:** Evaluating Selective, Sustained, and Divided Attention in 33 Frontier Language Models

**Track:** Attention (Cognitive Abilities)

---

## Project Name

Can AI Models Pay Attention? An Attention Benchmark for Frontier Language Models

---

## Your Team

Conrad Kleykamp (individual submission)

---

## Problem Statement

Attention is one of the most fundamental components of intelligence. Before a person can reason, plan, or remember, they must first be able to focus on what matters, ignore what does not, track information over time, and, when needed, monitor multiple things at once. These are not advanced cognitive feats. They are the baseline requirements for intelligent behavior in a complex world.

Despite this, attentional control has received little systematic attention as a lens for evaluating large language models (LLMs). Most benchmarks measure what models know or how well they reason. Far fewer ask whether a model can direct and sustain its attention in ways that mirror basic human cognitive function.

This benchmark addresses that gap. It evaluates 33 frontier language models across three attentional tasks drawn from established cognitive science: selective attention, sustained attention, and divided attention. The goal is to measure not just whether models get the right answer, but whether they can maintain the attentional discipline required to do so reliably.

---

## Task and Benchmark Construction

The benchmark consists of three tasks, each targeting a distinct type of attention. All tasks were evaluated across all 33 models available in the Kaggle environment.

**Selective Attention** tests the ability to extract goal-relevant information from a passage containing deliberate distractors. The distractors are plausible and contextually related, making them easy to accidentally include. Models must answer a specific question using only the relevant content.

**Sustained Attention** tests the ability to track and aggregate targets accurately across a sequential context of up to 15 records, without skipping entries, losing count, or approximating. Each scenario also includes a strict check on the final numeric answer, separate from the judge-evaluated criteria.

**Divided Attention** tests the ability to simultaneously monitor and reason across two independent information streams, keeping facts from each correctly attributed without conflation. Models are given two clearly labeled streams and must answer a question that requires drawing on both.

Selective attention uses 3 scenarios and 5 judge-evaluated criteria per scenario (15 assertions per model). Sustained attention uses 5 scenarios and 5 judge-evaluated criteria plus 1 regex hard-check per scenario (30 assertions per model). Divided attention uses 5 scenarios and 5 judge-evaluated criteria per scenario (25 assertions per model).

All responses are scored by a fixed external judge model (`kbench.judge_llm`) rather than by the model being tested. This eliminates self-evaluation bias and ensures scores are directly comparable across all 33 models.

---

## Dataset

Selective attention uses 3 handcrafted scenarios. Sustained and divided attention each use 5 scenarios spanning a range of difficulty levels. All scenarios were designed to isolate the target attentional behavior. Scenarios were written to be realistic, clearly structured, and free of ambiguity, so that failures reflect attentional lapses rather than unclear instructions.

**Selective Attention scenarios:**
- A corporate annual report mixing financial metrics with strategic announcements and headcount data. The model must extract only the financial performance figures.
- A clinical patient note mixing vital signs with unrelated personal details. The model must report only the clinical observations.
- A research study description mixing experimental findings with researcher background and funding information. The model must identify only the key methodology and results.

**Sustained Attention scenarios (5):**
- 15 financial transactions involving multiple named parties. The model must calculate one person's exact net balance across all transactions, showing all working.
- 14 days of weather records. The model must count how many days met two simultaneous conditions.
- 10 inventory items across multiple categories. The model must calculate the total inventory value for one specific category.
- 8 expense report entries across multiple employees and categories. The model must total one specific category.
- 12 server request log entries mixing two servers and two status types. The model must calculate the average response time for successful requests on one server only.

**Divided Attention scenarios (5):**
- Log files from two servers running in parallel. The model must report error counts per server and identify which error type appeared on both.
- Trade histories from two separate investment portfolios. The model must identify stocks appearing in both and determine which portfolio realized a profit on its sold positions.
- Sprint update logs from two separate engineering teams. The model must identify which team was blocked and on which day their work became directly dependent on each other.
- Academic records for two students. The model must identify who scored higher on a specific exam and who has the higher average across assignments only.
- Weekly production logs from two factories. The model must compare total output, total defects, and correctly attribute each factory's production halt to its distinct cause.

---

## Technical Details

The benchmark is implemented using the `kaggle-benchmarks` framework inside the Kaggle notebook environment, where `kaggle-benchmarks` is pre-installed and model access is provided via `kbench.llm`, `kbench.llms`, and `kbench.judge_llm`.

Each task is defined using the `@kbench.task` decorator, which registers the task function with the framework. Task data is defined as a `pandas` DataFrame (`TASK_DATA`) and passed to the task via `bind_dataframe`. The benchmark notebooks loop over all 33 available models using `kbench.llms`, running every task scenario against each model and collecting results.

Scenario counts differ across tasks because each was calibrated to the configuration that maximized performance discrimination across models. Additional scenarios improved discrimination for sustained and divided attention but compressed the performance spread for selective attention. Pass rates are used for all cross-task comparisons, making the differing totals transparent but not consequential for interpretation.

Responses are evaluated using two assertion types:

- `assess_response_with_judge`: sends the response and a list of criteria to the fixed judge model, which returns a pass/fail result for each criterion. Results are registered via `assert_true`.
- `assert_contains_regex`: a hard pattern check used in sustained attention to verify the final numeric answer independently of the judge.

A separate set of task notebooks (`*_task.ipynb`) is also provided for single-model evaluation via the Kaggle task runner. These use `kbench.llm` rather than `kbench.llms` and run each scenario row individually using `task.run()`.

---

## Results, Insights, and Conclusions

Evaluated across 33 models in the Kaggle environment. Full per-model breakdowns are available in the results CSVs and executed notebooks.

> **Note:** LLM outputs are non-deterministic and no random seed can be set for hosted models. Pass rates may vary slightly across runs. The figures below reflect a single full evaluation run.

| Task | Models | Avg Pass Rate | Top Score | Bottom Score |
|---|---|---|---|---|
| Selective Attention | 33 | 96.0% | 100% (18 models) | 66.7% |
| Sustained Attention | 33 | 97.5% | 100% (28 models) | 40.0% |
| Divided Attention | 33 | 92.6% | 100% (12 models) | 68.0% |

**Key findings:**

- Divided attention is the strongest discriminator across all 33 models: 8 distinct performance levels, a 32pp spread (100% to 68%), and only 12 of 33 models at a perfect score. No other task produces comparable separation between models at the same capability tier.
- Selective attention is well-calibrated at 4 distinct levels (100% to 66.7%), with 18 of 33 models at a perfect score and 13 more clustered at 93.3%. The spread is real but compressed near the top.
- Sustained attention exposes a ceiling effect: 28 of 33 models scored 100%, and the 5 remaining non-outlier models span only 10 percentage points (90% to 97%). It reliably identifies small-model failure but contributes little differentiation among frontier models.
- Only 5 models scored 100% across all three tasks: `claude-opus-4-1`, `claude-sonnet-4-6`, `deepseek-v3.1`, `gemini-3.1-pro-preview`, and `qwen3-235b-a22b-instruct-2507`.
- Divided attention reveals capability gaps invisible in the other tasks. `gpt-oss-120b` (76%), `gpt-5.4-mini` (80%), `gemma-3-12b` (84%), and `gemini-2.5-flash` (84%) all score 100% on sustained and at or near 100% on selective, yet drop significantly on divided. The task isolates a specific failure mode: maintaining numerical precision across two concurrent information streams.
- `gemma-3-1b` is the consistent low outlier across all three tasks (66.7% / 40.0% / 68.0%), with a particularly steep drop on sustained attention. It is the smallest model in the evaluated set by a significant margin.
- `gemini-2.0-flash` scores 100% on both sustained and divided while scoring only 86.7% on selective, a pattern suggesting relative strength in structured multi-step tasks versus single-passage distractor filtering.
- Per-criterion analysis identifies the exact failure modes. In divided attention, halt cause attribution in the factory scenario drives the majority of failures: 15 of 33 models incorrectly attributed Factory B's supply delay halt, and 14 of 33 failed Factory A's equipment calibration halt — the two highest individual criterion failure rates in the entire benchmark. Output totals and defect counts on the same scenario failed in only 2 and 1 models respectively, confirming the difficulty is cross-stream attribution under concurrent load, not arithmetic.
- In selective attention, 13 of 33 models failed a single criterion: not mentioning the lead researcher's hiking hobby in the research study scenario. This one distractor accounts for nearly all of selective attention's failures across all 33 models, and reflects a specific behavior — models summarize the full passage rather than filtering it to the task-relevant content.
- In sustained attention, the regex hard-check correctly flags 4 models that gave wrong final numeric answers on the Alice net balance scenario (`claude-haiku`, `claude-opus-4-6`, `gpt-oss-20b`, and `gemma-3-1b`). These are precisely the models that appear below 100% in the summary results, validating the dual-assertion design.

**Conclusions:**

The results reveal an interpretable and differentiated pattern across tasks. Selective attention is broadly well-supported at the frontier. Sustained attention is largely solved by current frontier models, but degrades sharply at smaller model sizes. Divided attention is the hardest task by discrimination: only 12 of 33 models achieved a perfect score, and failures cluster in scenarios requiring simultaneous numerical reasoning across both streams rather than in simpler stream-identification scenarios.

The most informative finding is the cross-task drop pattern combined with the per-criterion data. Several models that score 100% on both sustained and selective fall to 76-84% on divided, and the criterion-level data shows exactly why: the factory scenario's halt cause attribution criteria (15/33 and 14/33 failure rates) are the primary driver. Models can track two streams and aggregate numbers correctly, but confuse which event belongs to which stream when both streams contain similar event types. This is a precise and previously uncharacterized failure mode. Only 5 of 33 models scored 100% across all three tasks.

The ceiling effects are informative rather than problematic. High pass rates among top-tier models confirm the scenarios are well-formed and unambiguous. The spread below 100% is where real model differences emerge, and divided attention produces the most granular separation of any task in the benchmark: 8 distinct performance levels spanning 32 percentage points.

As LLMs are deployed in environments requiring long-context tracking, multi-stream reasoning, and robust distractor filtering, understanding attentional performance becomes increasingly important. This benchmark provides one concrete, grounded way to measure it across a large set of frontier models.

As LLMs are deployed in real-world environments that require long-context tracking, multi-stream reasoning, and robust distractor filtering, understanding attentional performance becomes increasingly important. This benchmark provides one concrete, grounded way to measure it.

---

## LLM Usage

Claude Code was used throughout this project as a development assistant, primarily for code tuning, implementation debugging, and refining task criteria wording. Task design, scenario selection, and all analytical judgements are my own.

---

## References and Citations

- Broadbent, D. E. (1958). *Perception and Communication.* Pergamon Press. (foundational model of selective attention)
- Treisman, A. M. (1964). Selective attention in man. *British Medical Bulletin, 20*(1), 12-16.
- Parasuraman, R. (1984). Sustained attention in detection and discrimination. In R. Parasuraman & D. R. Davies (Eds.), *Varieties of Attention.* Academic Press.
- Kahneman, D. (1973). *Attention and Effort.* Prentice-Hall. (foundational work on divided attention and cognitive load)
- Kaggle Benchmarks framework: [https://www.kaggle.com/competitions/kaggle-measuring-agi](https://www.kaggle.com/competitions/kaggle-measuring-agi)
