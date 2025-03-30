import pytest
import os
from datetime import datetime
from sqlings.state import AppState
from sqlings.exercises import Exercise, ExerciseResult
from sqlings.config import Config
from pathlib import Path


def test_app_state_initialization(tmp_path, monkeypatch):
    # Test AppState initialization
    config = Config()
    config.project_name = "test_project"
    config.cwd = tmp_path
    config._finished = ("Completed exercises:", [])
    
    # Create necessary files for the config
    toml_content = "[settings]\ndialect = \"duckdb\""
    (tmp_path / "sqlings.toml").write_text(toml_content)
    
    finished_content = "Completed exercises:\n"
    (tmp_path / "finished.txt").write_text(finished_content)
    
    # Create a mock exercise file
    exercise_dir = tmp_path / "exercises" / "01_basics"
    exercise_dir.mkdir(parents=True)
    exercise_path = exercise_dir / "exercise1.sql"
    exercise_path.write_text("SELECT * FROM table1")
    
    # Mock the analyze_result method to avoid database operations
    def mock_analyze_result(self, db_path):
        self._result = ExerciseResult(result=True, traceback=None)
    
    monkeypatch.setattr(Exercise, "analyze_result", mock_analyze_result)
    
    state = AppState(config)
    assert state.config == config
    assert isinstance(state._exercises, list)
    assert len(state._exercises) == 1
    assert state._next_exercise is not None


def test_app_state_refresh(tmp_path, monkeypatch):
    # Test AppState refresh
    config = Config()
    config.project_name = "test_project"
    config.cwd = tmp_path
    config._finished = ("Completed exercises:", [])
    
    # Create necessary files for the config
    toml_content = "[settings]\ndialect = \"duckdb\""
    (tmp_path / "sqlings.toml").write_text(toml_content)
    
    finished_content = "Completed exercises:\n"
    (tmp_path / "finished.txt").write_text(finished_content)
    
    # Create a mock exercise file
    exercise_dir = tmp_path / "exercises" / "01_basics"
    exercise_dir.mkdir(parents=True)
    exercise_path = exercise_dir / "exercise1.sql"
    exercise_path.write_text("SELECT * FROM table1")
    
    # Mock the analyze_result method to avoid database operations
    def mock_analyze_result(self, db_path):
        self._result = ExerciseResult(result=True, traceback=None)
    
    monkeypatch.setattr(Exercise, "analyze_result", mock_analyze_result)
    
    # Create a dummy database file
    (tmp_path / "sqlings.duckdb").touch()
    
    state = AppState(config)
    
    # Update the timestamp to simulate file modification
    old_timestamp = state._exercises[0].last_saved
    new_timestamp = old_timestamp + 100  # Add 100 seconds
    exercise_path.touch(exist_ok=True)
    
    # Mock os.path.getmtime to return our new timestamp
    def mock_getmtime(path):
        return new_timestamp
    
    monkeypatch.setattr("os.path.getmtime", mock_getmtime)
    
    state.refresh()
    
    assert state._exercises[0].result.result is True
    assert state._exercises[0].last_saved == new_timestamp


def test_get_next_exercise_no_finished(tmp_path, monkeypatch):
    # Test getting next exercise when no exercises are finished
    config = Config()
    config.project_name = "test_project"
    config.cwd = tmp_path
    config._finished = ("Completed exercises:", [])
    
    # Create necessary files for the config
    toml_content = "[settings]\ndialect = \"duckdb\""
    (tmp_path / "sqlings.toml").write_text(toml_content)
    
    finished_content = "Completed exercises:\n"
    (tmp_path / "finished.txt").write_text(finished_content)
    
    # Create a mock exercise file
    exercise_dir = tmp_path / "exercises" / "01_basics"
    exercise_dir.mkdir(parents=True)
    exercise_path = exercise_dir / "exercise1.sql"
    exercise_path.write_text("SELECT * FROM table1")
    
    # Mock the analyze_result method to avoid database operations
    def mock_analyze_result(self, db_path):
        self._result = ExerciseResult(result=False, traceback=None)
    
    monkeypatch.setattr(Exercise, "analyze_result", mock_analyze_result)
    
    # Create a dummy database file
    (tmp_path / "sqlings.duckdb").touch()
    
    state = AppState(config)
    next_exercise = state.get_next_exercise()
    assert next_exercise is not None
    assert next_exercise.name == "exercise1"


def test_get_next_exercise_with_finished(tmp_path, monkeypatch):
    # Test getting next exercise when some exercises are finished
    config = Config()
    config.project_name = "test_project"
    config.cwd = tmp_path
    config._finished = ("Completed exercises:", ["exercise1"])
    
    # Create necessary files for the config
    toml_content = "[settings]\ndialect = \"duckdb\""
    (tmp_path / "sqlings.toml").write_text(toml_content)
    
    finished_content = "Completed exercises:\nexercise1"
    (tmp_path / "finished.txt").write_text(finished_content)
    
    # Create mock exercise files
    exercise_dir = tmp_path / "exercises" / "01_basics"
    exercise_dir.mkdir(parents=True)
    exercise_path1 = exercise_dir / "exercise1.sql"
    exercise_path1.write_text("SELECT * FROM table1")
    exercise_path2 = exercise_dir / "exercise2.sql"
    exercise_path2.write_text("SELECT * FROM table2")
    
    # Mock the analyze_result method to avoid database operations
    def mock_analyze_result(self, db_path):
        if self.name == "exercise1":
            self._result = ExerciseResult(result=True, traceback=None)
        else:
            self._result = ExerciseResult(result=False, traceback=None)
    
    monkeypatch.setattr(Exercise, "analyze_result", mock_analyze_result)
    
    # Create a dummy database file
    (tmp_path / "sqlings.duckdb").touch()
    
    state = AppState(config)
    next_exercise = state.get_next_exercise()
    assert next_exercise is not None
    assert next_exercise.name == "exercise2"


def test_get_next_exercise_all_finished(tmp_path, monkeypatch):
    # Test getting next exercise when all exercises are finished
    config = Config()
    config.project_name = "test_project"
    config.cwd = tmp_path
    config._finished = ("Completed exercises:", ["exercise1", "exercise2"])
    
    # Create necessary files for the config
    toml_content = "[settings]\ndialect = \"duckdb\""
    (tmp_path / "sqlings.toml").write_text(toml_content)
    
    finished_content = "Completed exercises:\nexercise1\nexercise2"
    (tmp_path / "finished.txt").write_text(finished_content)
    
    # Create mock exercise files
    exercise_dir = tmp_path / "exercises" / "01_basics"
    exercise_dir.mkdir(parents=True)
    exercise_path1 = exercise_dir / "exercise1.sql"
    exercise_path1.write_text("SELECT * FROM table1")
    exercise_path2 = exercise_dir / "exercise2.sql"
    exercise_path2.write_text("SELECT * FROM table2")
    
    # Mock the analyze_result method to avoid database operations
    def mock_analyze_result(self, db_path):
        self._result = ExerciseResult(result=True, traceback=None)
    
    monkeypatch.setattr(Exercise, "analyze_result", mock_analyze_result)
    
    # Create a dummy database file
    (tmp_path / "sqlings.duckdb").touch()
    
    state = AppState(config)
    next_exercise = state.get_next_exercise()
    
    # When all exercises are finished, it should return the last exercise
    assert next_exercise is not None
    assert next_exercise.name == "exercise2"
