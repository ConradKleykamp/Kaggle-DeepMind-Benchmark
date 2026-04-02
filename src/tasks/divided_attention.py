import kaggle_benchmarks as kbench
import pandas as pd


TASK_DATA = pd.DataFrame([
    {
        "stream_a": (
            "Server A logs: "
            "09:00 - Request received from user_42. "
            "09:02 - Query executed successfully. "
            "09:05 - Request received from user_17. "
            "09:07 - ERROR: Timeout on database connection. "
            "09:10 - Request received from user_99. "
            "09:12 - Query executed successfully. "
            "09:15 - ERROR: Memory limit exceeded. "
            "09:18 - Request received from user_42. "
            "09:20 - Query executed successfully."
        ),
        "stream_b": (
            "Server B logs: "
            "09:01 - Request received from user_55. "
            "09:03 - Query executed successfully. "
            "09:06 - Request received from user_23. "
            "09:08 - Query executed successfully. "
            "09:11 - ERROR: Disk read failure. "
            "09:13 - Request received from user_77. "
            "09:16 - Query executed successfully. "
            "09:19 - ERROR: Timeout on database connection. "
            "09:21 - Request received from user_55."
        ),
        "question": (
            "Monitoring both server logs simultaneously: "
            "How many errors occurred on each server, "
            "and which error type appeared on both servers?"
        ),
        "criteria": [
            "Response correctly identifies 2 errors on Server A.",
            "Response correctly identifies 2 errors on Server B.",
            "Response identifies 'Timeout on database connection' as appearing on both servers.",
            "Response does not confuse errors between the two servers.",
            "Response addresses both streams without omitting either.",
        ],
    },
    {
        "stream_a": (
            "Portfolio A trades: "
            "Trade 1: Bought 50 shares of AAPL at $178. "
            "Trade 2: Sold 30 shares of GOOG at $142. "
            "Trade 3: Bought 100 shares of MSFT at $415. "
            "Trade 4: Sold 50 shares of AAPL at $185. "
            "Trade 5: Bought 20 shares of AMZN at $192."
        ),
        "stream_b": (
            "Portfolio B trades: "
            "Trade 1: Bought 80 shares of TSLA at $245. "
            "Trade 2: Bought 40 shares of GOOG at $140. "
            "Trade 3: Sold 80 shares of TSLA at $261. "
            "Trade 4: Sold 40 shares of NVDA at $875. "
            "Trade 5: Bought 60 shares of MSFT at $418."
        ),
        "question": (
            "Tracking both portfolios simultaneously: "
            "Which stock appears in both portfolios, "
            "and which portfolio realized a profit on its sold positions?"
        ),
        "criteria": [
            "Response correctly identifies GOOG and MSFT as appearing in both portfolios.",
            "Response correctly identifies Portfolio A realized profit on AAPL (bought at $178, sold at $185).",
            "Response correctly identifies Portfolio B realized profit on TSLA (bought at $245, sold at $261).",
            "Response correctly identifies Portfolio B realized profit on NVDA sold position.",
            "Response does not conflate trades between the two portfolios.",
        ],
    },
    {
        "stream_a": (
            "Team A sprint updates: "
            "Monday: Completed user authentication module. "
            "Tuesday: Started API integration, blocked on missing credentials. "
            "Wednesday: Credentials received, API integration resumed. "
            "Thursday: API integration completed and tested. "
            "Friday: Began dashboard UI development."
        ),
        "stream_b": (
            "Team B sprint updates: "
            "Monday: Completed database schema design. "
            "Tuesday: Started data migration scripts. "
            "Wednesday: Data migration 60% complete, no blockers. "
            "Thursday: Data migration completed. "
            "Friday: Started integration testing with Team A's API."
        ),
        "question": (
            "Tracking both team streams simultaneously: "
            "Which team experienced a blocker this sprint, "
            "and on which day did the two teams' work become directly dependent on each other?"
        ),
        "criteria": [
            "Response correctly identifies Team A as experiencing a blocker on Tuesday.",
            "Response correctly identifies the blocker as missing API credentials.",
            "Response correctly identifies Friday as the day Team B began depending on Team A's API.",
            "Response does not attribute Team B's progress as blocked.",
            "Response addresses both team streams without omitting either.",
        ],
    },
])


@kbench.task(name="divided_attention")
def divided_attention(
    llm,
    stream_a: str,
    stream_b: str,
    question: str,
    criteria: list,
):
    """
    Evaluating divided attention: model must simultaneously monitor and reason
    across two independent information streams without conflating them.
    """
    prompt = (
        f"You are given two independent information streams. "
        f"Read both carefully and answer the question by tracking each stream separately.\n\n"
        f"Stream A:\n{stream_a}\n\n"
        f"Stream B:\n{stream_b}\n\n"
        f"Question: {question}"
    )

    response = llm.prompt(prompt)

    kbench.assertions.assess_response_with_judge(
        criteria=criteria,
        response_text=response,
        judge_llm=llm,
    )