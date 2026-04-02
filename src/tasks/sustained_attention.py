import kaggle_benchmarks as kbench
import pandas as pd


TASK_DATA = pd.DataFrame([
    {
        "context": (
            "Transaction 1: Alice sent $200 to Bob. "
            "Transaction 2: Carol bought groceries for $45. "
            "Transaction 3: Bob transferred $80 to Dave. "
            "Transaction 4: Eve paid $120 for utilities. "
            "Transaction 5: Alice received $300 from Frank. "
            "Transaction 6: Dave spent $60 at a restaurant. "
            "Transaction 7: Carol received $150 from Grace. "
            "Transaction 8: Frank paid $90 for insurance. "
            "Transaction 9: Bob bought electronics for $400. "
            "Transaction 10: Eve received $250 from Alice. "
            "Transaction 11: Grace paid $30 for a subscription. "
            "Transaction 12: Dave received $110 from Carol. "
            "Transaction 13: Alice paid $75 for phone bills. "
            "Transaction 14: Frank spent $200 on travel. "
            "Transaction 15: Bob received $95 from Eve."
        ),
        "question": "What is Alice's net balance across all transactions? Show your working.",
        "expected_answer": "-225",
        "criteria": [
            "Response correctly identifies all transactions involving Alice.",
            "Response accounts for Alice sending $200 (debit).",
            "Response accounts for Alice receiving $300 from Frank (credit).",
            "Response accounts for Alice paying $75 for phone bills (debit).",
            "Response accounts for Eve receiving $250 from Alice (debit).",
            "Final net balance calculated is negative $225.",
        ],
    },
    {
        "context": (
            "Day 1: Temperature recorded at 18C, humidity 65%. "
            "Day 2: Temperature recorded at 21C, humidity 70%. "
            "Day 3: Temperature recorded at 17C, humidity 80%. "
            "Day 4: Temperature recorded at 23C, humidity 55%. "
            "Day 5: Temperature recorded at 19C, humidity 60%. "
            "Day 6: Temperature recorded at 25C, humidity 45%. "
            "Day 7: Temperature recorded at 22C, humidity 50%. "
            "Day 8: Temperature recorded at 16C, humidity 85%. "
            "Day 9: Temperature recorded at 20C, humidity 75%. "
            "Day 10: Temperature recorded at 24C, humidity 40%. "
            "Day 11: Temperature recorded at 18C, humidity 68%. "
            "Day 12: Temperature recorded at 21C, humidity 72%. "
            "Day 13: Temperature recorded at 26C, humidity 38%. "
            "Day 14: Temperature recorded at 15C, humidity 90%."
        ),
        "question": "How many days had both temperature above 20C and humidity below 60%?",
        "expected_answer": "3",
        "criteria": [
            "Response correctly identifies Day 6 as meeting both conditions (25C, 45%).",
            "Response correctly identifies Day 10 as meeting both conditions (24C, 40%).",
            "Response correctly identifies Day 13 as meeting both conditions (26C, 38%).",
            "Response correctly excludes days meeting only one condition.",
            "Final count given is 3 days.",
        ],
    },
    {
        "context": (
            "Item A: Category=Electronics, Price=$299, Stock=14 units. "
            "Item B: Category=Clothing, Price=$49, Stock=200 units. "
            "Item C: Category=Electronics, Price=$899, Stock=6 units. "
            "Item D: Category=Food, Price=$12, Stock=500 units. "
            "Item E: Category=Clothing, Price=$89, Stock=75 units. "
            "Item F: Category=Electronics, Price=$199, Stock=30 units. "
            "Item G: Category=Food, Price=$8, Stock=1000 units. "
            "Item H: Category=Clothing, Price=$129, Stock=40 units. "
            "Item I: Category=Electronics, Price=$649, Stock=9 units. "
            "Item J: Category=Food, Price=$22, Stock=300 units."
        ),
        "question": "What is the total inventory value of all Electronics items?",
        "expected_answer": "$21391",
        "criteria": [
            "Response identifies all four Electronics items: A, C, F, and I.",
            "Response correctly calculates Item A value as $4186 (299 x 14).",
            "Response correctly calculates Item C value as $5394 (899 x 6).",
            "Response correctly calculates Item F value as $5970 (199 x 30).",
            "Response correctly calculates Item I value as $5841 (649 x 9).",
            "Total inventory value calculated is $21391.",
        ],
    },
])


@kbench.task(name="sustained_attention")
def sustained_attention(
    llm,
    context: str,
    question: str,
    expected_answer: str,
    criteria: list,
):
    """
    Evaluating sustained attention: model must track and aggregate specific
    targets accurately across a long sequential context.
    """
    prompt = (
        f"Read the following records carefully and answer the question. "
        f"Track every relevant entry — do not skip or approximate.\n\n"
        f"Records:\n{context}\n\n"
        f"Question: {question}"
    )

    response = llm.prompt(prompt)

    kbench.assertions.assert_contains_regex(
        pattern=expected_answer,
        text=response,
        expectation=f"Response should contain the correct answer: {expected_answer}",
    )

    kbench.assertions.assess_response_with_judge(
        criteria=criteria,
        response_text=response,
        judge_llm=llm,
    )