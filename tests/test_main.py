import pytest
from click.testing import CliRunner
from sqlings.main import sqlings, new, start
from sqlings.config import Config
from pathlib import Path
from sqlings.helpers import copy_starter


def test_sqlings_command_group():
    # Test the sqlings command group
    runner = CliRunner()
    result = runner.invoke(sqlings, ["--help"])
    assert result.exit_code == 0
    assert "Welcome to SQLings, the best way to learn SQL" in result.output


def test_new_command(tmp_path, monkeypatch):
    # Test the new command using isolated_filesystem
    runner = CliRunner()
    
    with runner.isolated_filesystem() as fs:
        # Convert the filesystem path to a Path object
        fs_path = Path(fs)
        
        # Create a proper starter directory structure
        starter_path = fs_path / "starter"
        starter_path.mkdir()
        
        # Create exercises directory
        exercises_dir = starter_path / "exercises"
        exercises_dir.mkdir()
        
        # Add exercise files to the exercises directory
        (exercises_dir / "exercise1.sql").write_text("SELECT * FROM table1")
        (exercises_dir / "exercise2.sql").write_text("SELECT * FROM table2")
        
        # Add required config files
        (starter_path / "sqlings.toml").write_text("[settings]\ndialect = \"duckdb\"")
        (starter_path / "finished.txt").write_text("Completed exercises:\n")
        
        # Create a custom Config class that works with our test
        class TestConfig:
            def __init__(self):
                self.cwd = fs_path
                self._project_name = None
                self._finished = ("Completed exercises:", [])
                self._settings = {"settings": {"dialect": "duckdb"}}
            
            @property
            def project_name(self):
                return self._project_name
                
            @project_name.setter
            def project_name(self, value):
                self._project_name = value
                
            @property
            def finished(self):
                return self._finished[1]
                
            @property
            def settings(self):
                return self._settings
        
        # Create an instance to use in the test
        test_config = TestConfig()
        
        # Mock necessary components
        monkeypatch.setattr("sqlings.helpers.PACKAGE_PATH", fs_path)
        
        # Run the command with our test config
        result = runner.invoke(new, ["test_project"], obj=test_config)
        
        # Check the results
        assert result.exit_code == 0, f"Command failed with: {result.exception}"
        assert "Project test_project created successfully!" in result.output
        assert (fs_path / "test_project" / "exercises" / "exercise1.sql").exists()
        assert (fs_path / "test_project" / "exercises" / "exercise2.sql").exists()


def test_start_command(tmp_path, monkeypatch):
    # Test the start command
    runner = CliRunner()
    
    # Create a mock project directory
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    
    # Create mock exercise files
    exercise_dir = project_dir / "exercises"
    exercise_dir.mkdir()
    (exercise_dir / "exercise1.sql").write_text("SELECT * FROM table1")
    
    # Mock the SqlingsApp.run method
    class MockApp:
        def __init__(self, state, config):
            self.state = state
            self.config = config
        
        def run(self):
            pass
    
    monkeypatch.setattr("sqlings.ui.app.SqlingsApp", MockApp)
    
    # Change to project directory
    monkeypatch.chdir(project_dir)
    
    result = runner.invoke(start)
    assert result.exit_code == 0
