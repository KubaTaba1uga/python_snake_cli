import pytest

from src.game_engine.session import SessionDummy


def test_dummy_session():
    session = SessionDummy()

    with pytest.raises(NotImplementedError):
        session.board
