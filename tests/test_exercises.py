import pytest
from datetime import datetime
from pathlib import Path
from sqlings.exercises import Exercise, ExerciseResult
from sqlings.config import Config
from sqlings.helpers import get_db_connection
import os
import polars as pl


def test_exercise_initialization(mock_exercise_file):
    exercise = Exercise("exercise1", mock_exercise_file)
    assert exercise.name == "exercise1"
    assert exercise._path == mock_exercise_file
    assert exercise._skipped == False
    assert exercise._result is None


def test_exercise_last_saved(mock_exercise):
    # Test getting last saved timestamp
    timestamp = mock_exercise.last_saved
    assert isinstance(timestamp, float)
    assert timestamp > 0


def test_analyze_result_correct(mock_exercise, mock_get_db_connection):
    # Test analyze_result with correct solution
    mock_exercise.analyze_result(Path("mock_db"))
    assert mock_exercise.result.result is True
    assert mock_exercise.result.traceback is None


def test_analyze_result_incorrect(mock_exercise, mock_get_db_connection, monkeypatch):
    # Test analyze_result with incorrect solution
    class MockConnection:
        def sql(self, query):
            if "solution" in query:
                return pl.DataFrame({"column1": [1, 2, 3], "column2": ["a", "b", "c"]})
            else:
                return pl.DataFrame({"column1": [1, 2, 3], "column2": ["a", "b", "d"]})
        
        def close(self):
            pass
    
    monkeypatch.setattr("sqlings.exercises.get_db_connection", lambda _: MockConnection())
    
    mock_exercise.analyze_result(Path("mock_db"))
    assert mock_exercise.result.result is False
    assert mock_exercise.result.traceback is not None


def test_update_save_ts(mock_exercise):
    # Test updating save timestamp
    new_timestamp = datetime.now().timestamp()
    mock_exercise.update_save_ts(new_timestamp)
    assert mock_exercise.last_saved == new_timestamp
