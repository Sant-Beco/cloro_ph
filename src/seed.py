from sqlalchemy import select

from .database import SessionLocal
from .models import Site


DEFAULT_SITES = [
    {"name": "Granja Esperanza", "kind": "granja", "location": "Borotoma"},
    {"name": "Granja La Fe", "kind": "granja", "location": "Zona Rural"},
    {"name": "Planta de Incubacion", "kind": "incubacion", "location": "Planta Central"},
]


def seed_sites() -> None:
    with SessionLocal() as db:
        for site_data in DEFAULT_SITES:
            exists = db.scalar(select(Site).where(Site.name == site_data["name"]))
            if exists is None:
                db.add(Site(**site_data))
        db.commit()


if __name__ == "__main__":
    seed_sites()
    print("Sedes iniciales verificadas.")
