import pandas as pd
import pytest


# --- TASK_DATA structure ---

def test_selective_attention_task_data():
    from src.tasks.selective_attention import TASK_DATA
    assert isinstance(TASK_DATA, pd.DataFrame)
    assert len(TASK_DATA) > 0
    for col in ("context", "question", "distractors", "criteria"):
        assert col in TASK_DATA.columns, f"Missing column: {col}"


def test_sustained_attention_task_data():
    from src.tasks.sustained_attention import TASK_DATA
    assert isinstance(TASK_DATA, pd.DataFrame)
    assert len(TASK_DATA) > 0
    for col in ("context", "question", "expected_answer", "criteria"):
        assert col in TASK_DATA.columns, f"Missing column: {col}"


def test_divided_attention_task_data():
    from src.tasks.divided_attention import TASK_DATA
    assert isinstance(TASK_DATA, pd.DataFrame)
    assert len(TASK_DATA) > 0
    for col in ("stream_a", "stream_b", "question", "criteria"):
        assert col in TASK_DATA.columns, f"Missing column: {col}"


# --- Runner callables ---

def test_runner_callables():
    from src.evaluation.runner import run_all, save_results
    assert callable(run_all)
    assert callable(save_results)
