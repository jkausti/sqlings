import pytest
from sqlings.exceptions import (
    SqlingsDBException,
    SqlingsProjectException,
    SqlingsProjectDBExistsException,
)


def test_sqlings_db_exception():
    # Test basic SqlingsDBException
    with pytest.raises(SqlingsDBException):
        raise SqlingsDBException()


def test_sqlings_project_exception():
    # Test SqlingsProjectException with message
    message = "Test project error"
    with pytest.raises(SqlingsProjectException) as exc_info:
        raise SqlingsProjectException(message)
    assert str(exc_info.value) == message


def test_sqlings_project_db_exists_exception():
    # Test SqlingsProjectDBExistsException
    project_name = "test_project"
    with pytest.raises(SqlingsProjectDBExistsException) as exc_info:
        raise SqlingsProjectDBExistsException(project_name)
    
    expected_message = f"A database file for project {project_name} already exists on your system in '$HOME/.sqlings/'"
    assert str(exc_info.value) == expected_message
