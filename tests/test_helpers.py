import pytest
from pathlib import Path
import shutil
from sqlings.helpers import copy_starter, get_db_connection
from sqlings.exceptions import SqlingsProjectException, SqlingsDBException
import duckdb
from duckdb import DuckDBPyConnection


def test_copy_starter(tmp_path, monkeypatch):
    # Test successful copy
    project_path = tmp_path / "test_project"
    
    # Create a proper starter directory structure in tmp_path
    starter_path = tmp_path / "starter"
    starter_path.mkdir()
    
    # Create exercises directory in starter path
    exercises_dir = starter_path / "exercises"
    exercises_dir.mkdir()
    
    # Create mock exercise files in starter directory
    (exercises_dir / "exercise1.sql").write_text("SELECT * FROM table1")
    (exercises_dir / "exercise2.sql").write_text("SELECT * FROM table2")
    (exercises_dir / "exercise3.sql").write_text("SELECT * FROM table3")
    
    # Create a sqlings.toml file in the starter directory
    (starter_path / "sqlings.toml").write_text("[settings]\ndialect = \"duckdb\"")
    # Create a finished.txt file in the starter directory
    (starter_path / "finished.txt").write_text("Completed exercises:\n")
    
    # Mock the PACKAGE_PATH to point to our test directory
    monkeypatch.setattr("sqlings.helpers.PACKAGE_PATH", tmp_path)
    
    # Call the function to copy the starter files
    copy_starter(project_path)
    
    # Verify the files were copied correctly
    assert (project_path / "exercises" / "exercise1.sql").exists()
    assert (project_path / "exercises" / "exercise2.sql").exists()
    assert (project_path / "exercises" / "exercise3.sql").exists()


def test_copy_starter_existing_project(tmp_path):
    # Test copy when project already exists
    project_path = tmp_path / "test_project"
    project_path.mkdir()
    (project_path / "test_file.txt").touch()
    
    with pytest.raises(SqlingsProjectException):
        copy_starter(project_path)


def test_get_db_connection_existing_db(tmp_path):
    # Test getting connection to existing database
    db_path = tmp_path / "test.db"
    con = duckdb.connect(str(db_path))
    con.close()
    
    con = get_db_connection(db_path)
    assert isinstance(con, DuckDBPyConnection)


def test_get_db_connection_nonexistent_db():
    # Test getting connection to non-existent database
    db_path = Path("/nonexistent/db.path")
    with pytest.raises(SqlingsDBException):
        get_db_connection(db_path)


def test_get_db_connection_error(tmp_path, monkeypatch):
    # Test database connection error
    db_path = tmp_path / "test.db"
    con = duckdb.connect(str(db_path))
    con.close()
    
    def mock_connect(*args, **kwargs):
        raise Exception("Database error")
    
    monkeypatch.setattr("duckdb.connect", mock_connect)
    
    with pytest.raises(SqlingsDBException):
        get_db_connection(db_path)
