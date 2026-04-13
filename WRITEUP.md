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

Attention is fundamental to intelligence. Before reasoning or planning, a system must focus on what matters, ignore what does not, track information over time, and when needed, monitor multiple things at once.

Despite this, attentional control has received little systematic attention as a lens for evaluating LLMs. Most benchmarks measure what models know or how well they reason. Far fewer ask whether a model can direct and sustain its attention in ways that mirror basic cognitive function.

This benchmark addresses that gap. It evaluates frontier language models across three attentional tasks drawn from cognitive science: selective attention, sustained attention, and divided attention. The goal is to measure not just whether models get the right answer, but whether they can maintain the attentional discipline required to do so reliably.

---

## Task and Benchmark Construction

The benchmark consists of three tasks, each targeting a distinct type of attention.

**Selective Attention** tests the ability to extract goal-relevant information from a passage containing deliberate distractors. Distractors are plausible and contextually related, making them easy to accidentally include. Models must answer a specific question using only the relevant content.

**Sustained Attention** tests the ability to track and aggregate targets accurately across a sequential context of up to 15 records, without skipping entries, losing count, or approximating. Each scenario includes a strict regex check on the final numeric answer, separate from judge-evaluated criteria.

**Divided Attention** tests the ability to simultaneously monitor and reason across two independent information streams, keeping facts from each correctly attributed without conflation. Models are given two clearly labeled streams and must answer a question requiring both.

Selective attention uses 3 scenarios (15 assertions per model), sustained uses 5 scenarios with a regex hard-check per row (30 assertions), and divided uses 5 scenarios (25 assertions). All responses are scored by a fixed external judge (`kbench.judge_llm`), eliminating self-evaluation bias and ensuring scores are directly comparable.

---

## Dataset

All scenarios were handcrafted to isolate the target attentional behavior and written to be realistic, clearly structured, and unambiguous, so that failures reflect attentional lapses rather than unclear instructions.

**Selective Attention (3 scenarios):** Passages mixing financial, clinical, and research content with plausible distractors. Each requires extracting only the task-relevant subset.

**Sustained Attention (5 scenarios):** Sequential records requiring single-entity or single-category tracking across up to 15 entries: financial transactions, weather logs, inventory records, expense reports, and server request logs.

**Divided Attention (5 scenarios):** Paired parallel streams requiring simultaneous tracking and cross-stream reasoning: server logs, investment portfolios, engineering sprint logs, academic records, and factory production logs.

---

## Technical Details

The benchmark runs inside the Kaggle notebook environment using the `kaggle-benchmarks` framework. Each task is defined with the `@kbench.task` decorator and loops over all available models via `kbench.llms`. Two assertion types are used: `assess_response_with_judge` sends criteria to the fixed external judge, and `assert_contains_regex` independently verifies final numeric answers. Scenario counts differ across tasks because each was calibrated to the configuration that maximized performance discrimination.

**Prompting:** Each model receives a scenario-specific prompt containing the full context (passage, records, or dual streams) and a single explicit question, with no chain-of-thought instruction or output format constraint imposed. **Scoring:** Responses are evaluated against five task-specific criteria by a fixed external judge (`kbench.judge_llm`); sustained attention also applies a regex hard-check on the final numeric answer independently of the judge. The model's score is the fraction of criteria passed across all scenarios. **Iteration:** Scenarios were manually written and refined until they produced meaningful score separation across models, with additional scenarios added to sustained and divided attention where the initial set compressed scores near the ceiling.

---

## Results, Insights, and Conclusions

Full per-model breakdowns are available in the results CSVs, executed notebooks, and visualizations (heatmap and bar chart).

> **Note:** LLM outputs are non-deterministic and no random seed can be set for hosted models. Pass rates may vary slightly across runs. The figures below reflect a single full evaluation run.

| Task | Models | Avg Pass Rate | Top Score | Bottom Score |
|---|---|---|---|---|
| Selective Attention | 33 | 96.0% | 100% (18 models) | 66.7% |
| Sustained Attention | 33 | 93.3% | 100% (21 models) | 16.7% |
| Divided Attention | 33 | 92.6% | 100% (12 models) | 68.0% |

**Key findings:**

- Divided attention is the strongest discriminator: 8 distinct performance levels, a 32pp spread (100% to 68%), and only 12 of 33 models at a perfect score. No other task produces comparable separation between models at the same capability tier.
- Selective attention is well-calibrated at 4 distinct levels (100% to 66.7%), with 18 of 33 at a perfect score and 13 more clustered at 93.3%.
- Sustained attention shows strong discrimination: 21 of 33 models scored 100% and 8 distinct performance levels span 83 percentage points (100% to 16.7%). The harder tracking scenarios expose real differences among frontier models while still clearly identifying small-model failure at the bottom.
- Only 4 models scored 100% across all three tasks: `claude-opus-4-1`, `deepseek-v3.1`, `gemini-3.1-pro-preview`, and `qwen3-235b-a22b-instruct-2507`.
- Divided attention reveals capability gaps invisible in the other tasks. `gpt-5.4-mini` (80%), `gemini-2.5-pro` (88%), `gemma-4-26b-a4b` (88%), and `gemma-4-31b` (88%) all score 100% on both selective and sustained, yet drop significantly on divided. `gpt-oss-120b` (76%) shows the steepest divided attention drop despite near-perfect scores on the other two tasks.
- `gemma-3-1b` is the consistent low outlier across all three tasks (66.7% / 16.7% / 68.0%), with the steepest drop on sustained attention. It is the smallest model in the evaluated set by a significant margin.
- In divided attention, halt cause attribution in the factory scenario drives most failures: 15 of 33 models failed to attribute Factory B's supply delay halt, and 14 of 33 failed Factory A's equipment calibration halt, the two highest individual criterion failure rates in the benchmark. Output totals and defect counts on the same scenario failed in only 2 and 1 models respectively, confirming the difficulty is attribution under concurrent load, not arithmetic.
- In selective attention, 13 of 33 models failed a single criterion: not mentioning the lead researcher's hiking hobby. This one distractor accounts for nearly all of selective attention's failures, reflecting a tendency to summarize the full passage rather than filter to task-relevant content.
- In sustained attention, the customer support ticket log (row 4) is the hardest scenario: 6 of 33 models failed to correctly identify Morgan's resolved and unresolved ticket counts, with errors cascading into the unresolved percentage (5/33) and average resolution time (4/33). The payroll register (row 2) produced only 5 judge failures spread evenly across criteria, the easiest scenario in the task. The regex hard-check on the Alice net balance (row 0) flagged 6 models that produced incorrect final answers despite passing some judge criteria, confirming the dual-assertion design catches errors the judge alone would miss.

**Conclusions:**

The results reveal a clear and differentiated pattern. Selective attention is broadly well-supported at the frontier. Sustained attention discriminates meaningfully at harder difficulty levels while degrading sharply at smaller model sizes. Divided attention is the hardest task: only 12 of 33 models scored perfectly, and failures cluster in cross-stream attribution scenarios, not numerical aggregation.

The most informative finding is the cross-task drop pattern. Several models at 100% on both selective and sustained fall to 80-88% on divided. Criterion-level data pinpoints why: the factory halt attribution criteria (15/33 and 14/33 failure rates) drive most of this drop. Models can track two streams and aggregate numbers correctly, but confuse which event belongs to which stream when both contain similar event types. Only 4 of 33 models scored 100% across all three tasks.

As LLMs are deployed in environments requiring long-context tracking, multi-stream reasoning, and robust distractor filtering, understanding attentional performance becomes increasingly important. This benchmark provides one concrete, grounded way to measure it.

---

## LLM Usage

Claude Code was used throughout this project as a development assistant, primarily for code tuning, implementation debugging, and refining task criteria wording. Task design, scenario selection, and all analytical judgements are my own.

---

## References and Citations

- Broadbent, D. E. (1958). *Perception and Communication.* Pergamon Press.
- Treisman, A. M. (1964). Selective attention in man. *British Medical Bulletin, 20*(1), 12-16.
- Parasuraman, R. (1984). Sustained attention in detection and discrimination. In R. Parasuraman & D. R. Davies (Eds.), *Varieties of Attention.* Academic Press.
- Kahneman, D. (1973). *Attention and Effort.* Prentice-Hall.
- Kaggle Benchmarks framework: [https://www.kaggle.com/competitions/kaggle-measuring-agi](https://www.kaggle.com/competitions/kaggle-measuring-agi)
