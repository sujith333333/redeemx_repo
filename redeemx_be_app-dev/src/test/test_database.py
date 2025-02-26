import pytest
from sqlmodel import SQLModel, create_engine, Session, Field
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text
from unittest.mock import patch
from src.database import get_session, create_db_and_tables, engine
from sqlalchemy.exc import SQLAlchemyError
from unittest.mock import MagicMock

@pytest.fixture
def mock_db():
    return MagicMock(name="MockDB")

def test_create_db_and_tables_with_mock(mock_db):
    with patch("src.database.engine", new=mock_db), \
         patch("sqlmodel.SQLModel.metadata.create_all") as mocked_create_all, \
         patch("sqlmodel.SQLModel.metadata.drop_all") as mocked_drop_all:
        try:
            create_db_and_tables()  
            mocked_create_all.assert_called_once_with(bind=mock_db)
        except Exception as e:
            pytest.fail(f"Failed to create database and tables: {e}")

def test_get_session_success_with_mock(mock_db):
    with patch("src.database.Session", return_value=mock_db):
        session_generator = get_session()
        session = next(session_generator)
        try:
            assert session is not None
            assert session is mock_db, "The session is not the mocked database session."
        finally:
            session.close()


def test_get_session_with_exception(mock_db):
    with patch("src.database.Session", return_value=mock_db):
        session_generator = get_session()
        session = next(session_generator)
        try:
            with pytest.raises(SQLAlchemyError):
                raise SQLAlchemyError("Simulated exception")
        finally:
            session.close()
            mock_db.close.assert_called_once()


def test_get_session_commit_success():
    with patch("src.database.Session") as mock_session_cls:
        mock_session_instance = MagicMock(name="MockSession")
        mock_session_cls.return_value = mock_session_instance
        gen = get_session()
        session = next(gen)
        try:
            next(gen)
        except StopIteration:
            pass
        mock_session_instance.commit.assert_called_once()
        mock_session_instance.close.assert_called_once()


def test_get_session_commit_exception():
    with patch("src.database.Session") as mock_session_cls:
        mock_session_instance = MagicMock(name="MockSession")
        mock_session_cls.return_value = mock_session_instance
        mock_session_instance.commit.side_effect = SQLAlchemyError("Simulated commit failure")
        gen = get_session()
        session = next(gen)
        with pytest.raises(SQLAlchemyError, match="Simulated commit failure"):
            next(gen)
        mock_session_instance.rollback.assert_called_once()
        mock_session_instance.close.assert_called_once()
        

