import os
import uuid
from typing import List, Optional

from sqlalchemy import Boolean, Column, String, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session, declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ---------- Modelo ----------
class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    persona = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    completada = Column(Boolean, default=False)


# ---------- Sesión ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Repositorio ----------
def db_crear_tarea(db: Session, persona: str, descripcion: str, completada: bool) -> Tarea:
    tarea = Tarea(
        persona=persona,
        descripcion=descripcion,
        completada=completada
    )
    db.add(tarea)
    db.commit()
    db.refresh(tarea)
    return tarea


def db_obtener_tareas(db: Session) -> List[Tarea]:
    return db.query(Tarea).all()


def db_obtener_tarea(db: Session, tarea_id: uuid.UUID) -> Optional[Tarea]:
    return db.query(Tarea).filter(Tarea.id == tarea_id).first()


def db_actualizar_tarea(
    db: Session,
    tarea: Tarea,
    persona: str,
    descripcion: str,
    completada: bool
) -> Tarea:
    tarea.persona = persona
    tarea.descripcion = descripcion
    tarea.completada = completada
    db.commit()
    db.refresh(tarea)
    return tarea


def db_borrar_tarea(db: Session, tarea: Tarea) -> None:
    db.delete(tarea)
    db.commit()