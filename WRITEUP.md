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
| Selective Attention | 33 | 95.2% | 100% (14 models) | 73.3% |
| Sustained Attention | 33 | 96.8% | 100% (25 models) | 36.7% |
| Divided Attention | 33 | 93.6% | 100% (16 models) | 68.0% |

**Key findings:**

- Divided attention is the most discriminating task: 7 distinct performance levels, a 32pp spread (100% to 68%), and only 16 of 33 models at a perfect score. Multi-stream reasoning with numerical content is the hardest attentional demand tested.
- Selective attention shows a consistent spread: 14 of 33 models scored 100% and no model scored below 73.3%, with a 26.7pp range driven largely by smaller models.
- Sustained attention has the highest average (96.8%) but a bimodal distribution: 25 of 33 models scored 100%, while the remaining 8 spread between 90% and 36.7%. The task is well-handled by most frontier models but exposes significant weaknesses in smaller ones.
- `gemma-3-1b` is a consistent low outlier across all three tasks (73.3% / 36.7% / 68.0%), with a particularly steep drop on sustained attention. It is the smallest model in the evaluated set by a significant margin, suggesting attentional control degrades sharply at smaller model sizes.
- `gemini-2.0-flash` underperforms its generation on selective (80%) and scores below the median on divided (92%), while `gemini-2.0-flash-lite` scores 100% on sustained, suggesting that training differences rather than generation number determine attentional performance.
- Per-row analysis in the executed notebook outputs indicates that failures in divided attention cluster in scenarios requiring simultaneous numerical reasoning across both streams. Simpler stream-identification scenarios show near-universal pass rates even among weaker models, suggesting that the challenge is not dual-stream tracking per se but maintaining numerical precision across two concurrent contexts.

**Conclusions:**

The results reveal an interpretable pattern. Selective attention is broadly well-supported at the frontier, likely because filtering irrelevant content from a single passage is a task type well-represented in model training. Divided attention is the hardest task by discrimination: only 16 of 33 models achieved a perfect score, and failures cluster specifically in scenarios that require simultaneous numerical reasoning across both streams. Sustained attention sits in between: most frontier models handle it well, but smaller models degrade sharply.

The ceiling effects are informative rather than problematic. High pass rates among top-tier models confirm that the scenarios are well-formed and unambiguous. The spread below 90% is where real model differences emerge, and divided attention in particular produces the most granular separation of any task in this benchmark.

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
