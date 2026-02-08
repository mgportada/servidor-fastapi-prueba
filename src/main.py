from typing import List, Optional
from uuid import UUID

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

# Importa tus funciones y clases de la base de datos aquí:
from database import (db_actualizar_tarea, db_borrar_tarea, db_crear_tarea,
                      db_obtener_tarea, db_obtener_tareas, get_db)
from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class TareaBase(BaseModel):
    persona: str
    descripcion: str
    completada: bool = False

class TareaCreate(TareaBase):
    pass

class Tarea(TareaBase):
    id: UUID

    class Config:
        orm_mode = True  # Para que Pydantic pueda leer objetos ORM

# POST (Create)
@app.post("/tareas/", status_code=201, response_model=Tarea)
def crear_tarea(tarea: TareaCreate, db: Session = Depends(get_db)):
    nueva_tarea = db_crear_tarea(
        db=db,
        persona=tarea.persona,
        descripcion=tarea.descripcion,
        completada=tarea.completada,
    )
    return nueva_tarea

# GET (Read all)
@app.get("/tareas/", response_model=List[Tarea])
def listar_tareas(db: Session = Depends(get_db)):
    tareas = db_obtener_tareas(db)
    return tareas

# GET (Read one)
@app.get("/tareas/{tarea_id}", response_model=Tarea)
def obtener_tarea(tarea_id: UUID, db: Session = Depends(get_db)):
    tarea = db_obtener_tarea(db, tarea_id)
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea

# PUT (Update)
@app.put("/tareas/{tarea_id}", response_model=Tarea)
def actualizar_tarea(tarea_id: UUID, tarea_actualizada: TareaBase, db: Session = Depends(get_db)):
    tarea = db_obtener_tarea(db, tarea_id)
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    tarea_actualizada_db = db_actualizar_tarea(
        db=db,
        tarea=tarea,
        persona=tarea_actualizada.persona,
        descripcion=tarea_actualizada.descripcion,
        completada=tarea_actualizada.completada,
    )
    return tarea_actualizada_db

# DELETE (Delete)
@app.delete("/tareas/{tarea_id}", status_code=204)
def borrar_tarea(tarea_id: UUID, db: Session = Depends(get_db)):
    tarea = db_obtener_tarea(db, tarea_id)
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    db_borrar_tarea(db, tarea)
    return