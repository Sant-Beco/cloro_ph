import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.main import app
from src.models import Base, Site


@pytest.fixture()
def client() -> TestClient:
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    with TestingSessionLocal() as db:
        db.add_all(
            [
                Site(name="Granja Esperanza", kind="granja", location="Borotoma"),
                Site(name="Granja La Fe", kind="granja", location="Zona Rural"),
                Site(name="Planta de Incubacion", kind="incubacion", location="Planta Central"),
            ]
        )
        db.commit()

    def override_get_db() -> Session:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    from src.database import get_db

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()
