import os
import pandas as pd
import kaggle_benchmarks as kbench

from src.tasks.selective_attention import (
    selective_attention,
    TASK_DATA as SELECTIVE_TASK_DATA,
)
from src.tasks.sustained_attention import (
    sustained_attention,
    TASK_DATA as SUSTAINED_TASK_DATA,
)
from src.tasks.divided_attention import (
    divided_attention,
    TASK_DATA as DIVIDED_TASK_DATA,
)

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "results")


def run_selective_attention() -> list[dict]:
    records = []
    for i, row in SELECTIVE_TASK_DATA.iterrows():
        result = selective_attention.run(
            llm=kbench.llm,
            context=row["context"],
            question=row["question"],
            distractors=row["distractors"],
            criteria=row["criteria"],
        )
        records.append({
            "task": "selective_attention",
            "row_index": i,
            "question": row["question"],
            **vars(result),
        })
    return records


def run_sustained_attention() -> list[dict]:
    records = []
    for i, row in SUSTAINED_TASK_DATA.iterrows():
        result = sustained_attention.run(
            llm=kbench.llm,
            context=row["context"],
            question=row["question"],
            expected_answer=row["expected_answer"],
            criteria=row["criteria"],
        )
        records.append({
            "task": "sustained_attention",
            "row_index": i,
            "question": row["question"],
            **vars(result),
        })
    return records


def run_divided_attention() -> list[dict]:
    records = []
    for i, row in DIVIDED_TASK_DATA.iterrows():
        result = divided_attention.run(
            llm=kbench.llm,
            stream_a=row["stream_a"],
            stream_b=row["stream_b"],
            question=row["question"],
            criteria=row["criteria"],
        )
        records.append({
            "task": "divided_attention",
            "row_index": i,
            "question": row["question"],
            **vars(result),
        })
    return records


def run_all() -> pd.DataFrame:
    records = []
    records.extend(run_selective_attention())
    records.extend(run_sustained_attention())
    records.extend(run_divided_attention())
    return pd.DataFrame(records)


def save_results(df: pd.DataFrame, filename: str = "attention_results.csv") -> str:
    os.makedirs(RESULTS_DIR, exist_ok=True)
    output_path = os.path.join(RESULTS_DIR, filename)
    df.to_csv(output_path, index=False)
    return output_path


if __name__ == "__main__":
    results_df = run_all()
    output_path = save_results(results_df)
    print(f"Results saved to {output_path}")
    print(results_df.to_string())
