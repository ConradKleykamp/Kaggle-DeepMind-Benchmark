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

Each task contains 3 scenarios. Selective and divided attention use 5 judge-evaluated criteria per scenario (15 assertions per model). Sustained attention uses 5 judge-evaluated criteria plus 1 regex hard-check per scenario (18 assertions per model).

All responses are scored by a fixed external judge model (`kbench.judge_llm`) rather than by the model being tested. This eliminates self-evaluation bias and ensures scores are directly comparable across all 33 models.

---

## Dataset

Each task uses 3 handcrafted scenarios designed to isolate the target attentional behavior. Scenarios were written to be realistic, clearly structured, and free of ambiguity, so that failures reflect attentional lapses rather than unclear instructions.

**Selective Attention scenarios:**
- A corporate annual report mixing financial metrics with strategic announcements and headcount data. The model must extract only the financial performance figures.
- A clinical patient note mixing vital signs with unrelated personal details. The model must report only the clinical observations.
- A research study description mixing experimental findings with researcher background and funding information. The model must identify only the key methodology and results.

**Sustained Attention scenarios:**
- 15 financial transactions involving multiple named parties. The model must calculate one person's exact net balance across all transactions, showing all working.
- 14 days of weather records. The model must count how many days met two simultaneous conditions.
- 10 inventory items across multiple categories. The model must calculate the total inventory value for one specific category.

**Divided Attention scenarios:**
- Log files from two servers running in parallel. The model must report error counts per server and identify which error type appeared on both.
- Trade histories from two separate investment portfolios. The model must identify stocks appearing in both and determine which portfolio realized a profit on its sold positions.
- Sprint update logs from two separate engineering teams. The model must identify which team was blocked and on which day their work became directly dependent on each other.

---

## Technical Details

The benchmark is implemented using the `kaggle-benchmarks` framework inside the Kaggle notebook environment, where `kaggle-benchmarks` is pre-installed and model access is provided via `kbench.llm`, `kbench.llms`, and `kbench.judge_llm`.

Each task is defined using the `@kbench.task` decorator, which registers the task function with the framework. Task data is defined as a `pandas` DataFrame (`TASK_DATA`) and passed to the task via `bind_dataframe`. The benchmark notebooks loop over all 33 available models using `kbench.llms`, running every task scenario against each model and collecting results.

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
| Sustained Attention | 33 | 90.9% | 94.4% (24 models) | 33.3% |
| Divided Attention | 33 | 91.3% | 93.3% (27 models) | 66.7% |

**Key findings:**

- Selective attention is the strongest task overall: 14 of 33 models achieved a perfect score, and no model scored below 73.3%.
- No model scored 100% on sustained or divided attention, confirming these tasks impose a measurable ceiling even for frontier models.
- The performance hierarchy holds across all 33 models: selective attention outperforms both sustained and divided, which score similarly to each other. Distractor filtering appears to be better supported in current LLMs than sequential tracking or simultaneous stream management.
- `gemma-3-1b` is a consistent low outlier across all three tasks (73.3% / 33.3% / 66.7%), with a particularly steep drop on sustained attention. It is the smallest model in the evaluated set by a significant margin, suggesting attentional control degrades sharply at smaller model sizes.
- `gemini-2.0-flash` underperforms its newer variants on selective (80%) and sustained (77.8%), while `gemini-2.0-flash-lite` scores 94.4% on sustained, suggesting that generation number alone does not predict attentional performance.

**Conclusions:**

The results reveal a consistent and interpretable pattern. Selective attention is broadly well-supported at the frontier, likely because filtering irrelevant content from a single passage is a task type well-represented in model training. Sustained and divided attention are harder, and no model has mastered either.

The shared difficulty of sustained and divided attention points to a common underlying challenge: maintaining structure across a context that is designed to require effort or track multiple things simultaneously. This is distinct from general reading comprehension, and the benchmark results suggest it is an area where current models still have meaningful room to improve.

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
