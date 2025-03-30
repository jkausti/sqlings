import pytest
from sqlings.config import Config

def test_project_name(config):
    assert config.project_name == "test_project"

def test_read_finished(config):
    header, exercises = config.read_finished()
    assert header == "Completed exercises:"
    assert exercises == ["ex1", "ex2"]

def test_update_finished(config):
    config.update_finished("ex3")
    assert "ex3" in config.finished
    
def test_remove_finished(config):
    config.remove_finished("ex1")
    assert "ex1" not in config.finished

def test_settings(config):
    assert config.settings["settings"]["dialect"] == "duckdb"
