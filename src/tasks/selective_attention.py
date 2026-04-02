import kaggle_benchmarks as kbench
import pandas as pd


TASK_DATA = pd.DataFrame([
    {
        "context": (
            "The annual report stated that revenue grew by 12% in Q3. "
            "The marketing team launched three new campaigns in August. "
            "Operating costs fell by 4% due to supply chain improvements. "
            "The CEO mentioned plans to expand into Asian markets next year. "
            "Employee headcount increased by 200 in the past quarter. "
            "Net profit margin improved from 8.1% to 9.6% year-over-year."
        ),
        "question": "What financial performance metrics are reported?",
        "distractors": ["marketing campaigns", "Asian market expansion", "headcount"],
        "criteria": [
            "Response includes the 12% revenue growth in Q3.",
            "Response includes the 4% reduction in operating costs.",
            "Response includes the improvement in net profit margin from 8.1% to 9.6%.",
            "Response does not focus on marketing campaigns or headcount as financial metrics.",
        ],
    },
    {
        "context": (
            "The patient presented with a fever of 101.3F and mild cough. "
            "She mentioned her dog recently had surgery for a broken leg. "
            "Blood pressure was recorded at 118/76 mmHg. "
            "Her teenage son started college last month. "
            "Oxygen saturation measured at 97%. "
            "The patient reported occasional headaches over the past week. "
            "Her neighbor recommended a new restaurant downtown."
        ),
        "question": "What are the patient's clinical observations?",
        "distractors": ["dog surgery", "son starting college", "restaurant recommendation"],
        "criteria": [
            "Response includes the fever of 101.3F.",
            "Response includes the blood pressure reading of 118/76 mmHg.",
            "Response includes oxygen saturation of 97%.",
            "Response includes the mild cough and occasional headaches.",
            "Response excludes irrelevant personal details about the dog, son, or restaurant.",
        ],
    },
    {
        "context": (
            "The experiment used a sample size of 342 participants aged 18-65. "
            "The lead researcher enjoys hiking on weekends. "
            "Treatment group showed a 23% reduction in symptoms after 8 weeks. "
            "Data collection took place across four university hospitals. "
            "The control group received a placebo with no significant changes observed. "
            "Funding was provided by a private health foundation. "
            "Three participants withdrew due to personal reasons unrelated to the study."
        ),
        "question": "What were the key experimental findings and methodology?",
        "distractors": ["researcher hobbies", "funding source", "withdrawal reasons"],
        "criteria": [
            "Response includes the sample size of 342 participants.",
            "Response includes the 23% symptom reduction in the treatment group.",
            "Response includes the placebo control group outcome.",
            "Response includes the 8-week treatment duration.",
            "Response does not dwell on the researcher's hobbies or unrelated withdrawal reasons.",
        ],
    },
])


@kbench.task(name="selective_attention")
def selective_attention(
    llm,
    context: str,
    question: str,
    distractors: list,
    criteria: list,
):
    """
    Evaluating selective attention: model must extract goal-relevant information
    from a passage containing embedded distractors.
    """
    prompt = (
        f"Read the following passage carefully and answer the question. "
        f"Focus only on information directly relevant to the question.\n\n"
        f"Passage:\n{context}\n\n"
        f"Question: {question}"
    )

    response = llm.prompt(prompt)

    report = kbench.assertions.assess_response_with_judge(
        criteria=criteria,
        response_text=response,
        judge_llm=llm,
    )
    for result in report.results:
        kbench.assertions.assert_true(
            result.passed,
            expectation=result.criterion,
        )