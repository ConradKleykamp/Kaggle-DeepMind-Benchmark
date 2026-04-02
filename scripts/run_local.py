"""
Local dry-run inspection tool for all three attention tasks.

NOTE: Live model execution requires running inside a Kaggle notebook
environment where credentials (MODEL_PROXY_URL, MODEL_PROXY_API_KEY,
LLM_DEFAULT) are auto-injected. This script makes NO API calls —
it only loads task data and prints a structured preview of what
would be sent to the model for each task row.

Run from project root:
    python -m scripts.run_local
"""

from src.tasks.selective_attention import TASK_DATA as SELECTIVE_TASK_DATA
from src.tasks.sustained_attention import TASK_DATA as SUSTAINED_TASK_DATA
from src.tasks.divided_attention import TASK_DATA as DIVIDED_TASK_DATA

DIVIDER = "=" * 64
SECTION = "-" * 64


def _print_header(task_name: str, total_rows: int):
    print(f"\n{DIVIDER}")
    print(f"  TASK: {task_name}  ({total_rows} rows)")
    print(DIVIDER)


def _print_row(index: int, fields: dict):
    print(f"\n  Row {index}")
    print(f"  {SECTION}")
    for label, value in fields.items():
        if isinstance(value, list):
            print(f"  {label}:")
            for item in value:
                print(f"    - {item}")
        else:
            # Wrap long strings at 60 chars for readability
            lines = [value[i:i + 60] for i in range(0, len(value), 60)]
            print(f"  {label}: {lines[0]}")
            for line in lines[1:]:
                print(f"    {line}")


def preview_selective_attention():
    _print_header("selective_attention", len(SELECTIVE_TASK_DATA))
    for i, row in SELECTIVE_TASK_DATA.iterrows():
        _print_row(i, {
            "context":    row["context"],
            "question":   row["question"],
            "distractors": row["distractors"],
            "criteria":   row["criteria"],
        })


def preview_sustained_attention():
    _print_header("sustained_attention", len(SUSTAINED_TASK_DATA))
    for i, row in SUSTAINED_TASK_DATA.iterrows():
        _print_row(i, {
            "context":        row["context"],
            "question":       row["question"],
            "expected_answer": row["expected_answer"],
            "criteria":       row["criteria"],
        })


def preview_divided_attention():
    _print_header("divided_attention", len(DIVIDED_TASK_DATA))
    for i, row in DIVIDED_TASK_DATA.iterrows():
        _print_row(i, {
            "stream_a": row["stream_a"],
            "stream_b": row["stream_b"],
            "question": row["question"],
            "criteria": row["criteria"],
        })


def main():
    print(DIVIDER)
    print("  DRY-RUN MODE — no API calls will be made")
    print("  Live execution requires a Kaggle notebook environment")
    print(DIVIDER)

    preview_selective_attention()
    preview_sustained_attention()
    preview_divided_attention()

    total = len(SELECTIVE_TASK_DATA) + len(SUSTAINED_TASK_DATA) + len(DIVIDED_TASK_DATA)
    print(f"\n{DIVIDER}")
    print(f"  {total} task rows previewed across 3 tasks")
    print(DIVIDER)


if __name__ == "__main__":
    main()
