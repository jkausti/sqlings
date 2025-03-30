import pytest
from pathlib import Path
from sqlings.config import Config
from datetime import datetime
from sqlings.exercises import Exercise, ExerciseResult
from sqlings.helpers import get_db_connection
import os
import polars as pl

@pytest.fixture
def mock_project_dir(tmp_path: Path) -> Path:
    # Create a temporary project directory with required files
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    
    # Create sqlings.toml
    toml_content = """
[settings]
dialect = "duckdb"
"""
    (project_dir / "sqlings.toml").write_text(toml_content)
    
    # Create finished.txt
    finished_content = "Completed exercises:\nex1\nex2"
    (project_dir / "finished.txt").write_text(finished_content)
    
    return project_dir

@pytest.fixture
def config(mock_project_dir: Path, monkeypatch: pytest.MonkeyPatch) -> Config:
    # Patch cwd to return our mock directory
    monkeypatch.chdir(mock_project_dir)
    return Config()

@pytest.fixture
def mock_exercise_file(tmp_path):
    # Create a mock exercise file
    exercise_dir = tmp_path / "exercises"
    exercise_dir.mkdir()
    
    exercise_content = """
SELECT * FROM table1
WHERE column1 > 10
ORDER BY column2 DESC
LIMIT 10
"""
    
    exercise_path = exercise_dir / "exercise1.sql"
    exercise_path.write_text(exercise_content)
    
    return exercise_path

@pytest.fixture
def mock_solution_file(tmp_path):
    # Create a mock solution file
    solution_dir = tmp_path / "solutions"
    solution_dir.mkdir()
    
    solution_content = """
SELECT column1, column2 FROM table1
WHERE column1 > 10 AND column2 IS NOT NULL
ORDER BY column2 DESC
LIMIT 10
"""
    
    solution_path = solution_dir / "exercise1.sql"
    solution_path.write_text(solution_content)
    
    return solution_path

@pytest.fixture
def mock_exercise(mock_exercise_file, mock_solution_file, monkeypatch):
    # Create a mock exercise instance
    exercise = Exercise("exercise1", mock_exercise_file)
    
    # Set up the mock solution
    solution_content = mock_solution_file.read_text()
    
    # Mock the solution_sql property
    class MockSolutionProperty:
        def __get__(self, instance, owner):
            return solution_content
    
    monkeypatch.setattr(Exercise, "solution_sql", MockSolutionProperty(), raising=False)
    
    return exercise

@pytest.fixture
def mock_db_path(tmp_path):
    db_path = tmp_path / "test.db"
    db_path.touch()
    return db_path

@pytest.fixture
def mock_db_connection(mock_db_path):
    # Create a mock database connection
    class MockDataFrame:
        def __init__(self, data):
            self._df = pl.DataFrame(data)
        
        def pl(self):
            return self._df

    return MockDataFrame({"column1": [1, 2, 3], "column2": ["a", "b", "c"]})

@pytest.fixture
def mock_get_db_connection(monkeypatch, mock_db_connection):
    # Mock the get_db_connection function
    def mock_get_connection(db_path):
        class MockConnection:
            def sql(self, query):
                return mock_db_connection
            
            def close(self):
                pass
        return MockConnection()
    
    monkeypatch.setattr("sqlings.exercises.get_db_connection", mock_get_connection)
    monkeypatch.setattr("sqlings.helpers.get_db_connection", mock_get_connection)
    return mock_get_connection

@pytest.fixture
def mock_app_state(config, monkeypatch):
    class MockAppState:
        def __init__(self, config):
            self.config = config
            self._exercises = []
            self._next_exercise = None

        def refresh(self):
            pass

        def get_next_exercise(self):
            return None

    return MockAppState(config)
