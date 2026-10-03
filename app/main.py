from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db, init_db

app = FastAPI()

@app.get("/clients/", response_model=List[schemas.ClientResponse])
def list_clients(db: Session = Depends(get_db)):
    return crud.get_all_clients(db)

@app.post("/clients/", response_model=schemas.ClientResponse)
def add_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    return crud.create_client(db, client)

@app.put("/clients/{client_id}", response_model=schemas.ClientResponse)
def edit_client(client_id: int, client_update: schemas.ClientUpdate, db: Session = Depends(get_db)):
    result = crud.update_client(db, client_id, client_update)
    if not result:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return result

@app.delete("/clients/{client_id}", response_model=schemas.ClientResponse)
def remove_client(client_id: int, db: Session = Depends(get_db)):
    result = crud.delete_client(db, client_id)
    if not result:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return result

# --- Тренировки ---

@app.get("/workouts/", response_model=List[schemas.WorkoutResponse])
def list_workouts(db: Session = Depends(get_db)):
    return crud.get_all_workouts(db)

@app.post("/workouts/", response_model=schemas.WorkoutResponse)
def add_workout(workout: schemas.WorkoutCreate, db: Session = Depends(get_db)):
    result = crud.create_workout(db, workout)
    if result is None:
        raise HTTPException(
            status_code=400,
            detail="Не удалось создать тренировку: клиент не найден, неверный тип или недостаточно средств на балансе"
        )
    return result

@app.put("/workouts/{workout_id}", response_model=schemas.WorkoutResponse)
def edit_workout(workout_id: int, workout_update: schemas.WorkoutUpdate, db: Session = Depends(get_db)):
    result = crud.update_workout(db, workout_id, workout_update)
    if not result:
        raise HTTPException(status_code=404, detail="Тренировка не найдена")
    return result

@app.delete("/workouts/{workout_id}", response_model=schemas.WorkoutResponse)
def remove_workout(workout_id: int, db: Session = Depends(get_db)):
    result = crud.delete_workout(db, workout_id)
    if not result:
        raise HTTPException(status_code=404, detail="Тренировка не найдена")
    return result

# Создаём таблицы при старте
init_db()