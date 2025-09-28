import pytest
from sqlalchemy import create_engine
from src.db.database import Base
@pytest.fixture
def temp_engine():
    engine=create_engine("sqlite:///:memory:", echo=False, future=True)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()