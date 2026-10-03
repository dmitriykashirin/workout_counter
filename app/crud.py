from typing import List
from datetime import date
from sqlalchemy.orm import Session
from app import models, schemas


# ============ КЛИЕНТЫ ============

def create_client(db: Session, client: schemas.ClientCreate) -> schemas.ClientResponse:
    db_client = models.Client(
        name=client.name,
        price_per_session=client.price_per_session,
        package_balance=client.package_balance,
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return schemas.ClientResponse.model_validate(db_client)

def get_all_clients(db: Session) -> List[schemas.ClientResponse]:
    clients = db.query(models.Client).all()
    return [schemas.ClientResponse.model_validate(c) for c in clients]

def get_client_by_id(db: Session, client_id: int) -> models.Client:
    return db.query(models.Client).filter(models.Client.id == client_id).first()


def update_client(db: Session, client_id: int, client_update: schemas.ClientUpdate):
    db_client = get_client_by_id(db, client_id)
    if not db_client:
        return None

    update_data = client_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_client, field, value)

    db.commit()
    db.refresh(db_client)
    return schemas.ClientResponse.model_validate(db_client)


def delete_client(db: Session, client_id: int):
    db_client = get_client_by_id(db, client_id)
    if not db_client:
        return None
    db.delete(db_client)
    db.commit()
    return schemas.ClientResponse.model_validate(db_client)


def create_workout(db: Session, workout: schemas.WorkoutCreate) -> schemas.WorkoutResponse:
    client = get_client_by_id(db, workout.client_id)
    if not client:
        return None

    # Считаем стоимость
    if workout.workout_type == "ПТ":
        total_cost = client.price_per_session
    elif workout.workout_type == "Сплит":
        total_cost = client.price_per_session * 0.75
    else:
        return None

    # Проверяем баланс ДО создания тренировки
    if client.package_balance < total_cost:
        return None  # Недостаточно средств, сначала пополните

    # Создаём тренировку
    db_workout = models.Workout(
        client_id=workout.client_id,
        workout_date=workout.workout_date,
        workout_type=workout.workout_type,
        total_cost=total_cost,
    )
    db.add(db_workout)

    # Списываем деньги
    client.package_balance -= total_cost

    db.commit()
    db.refresh(db_workout)
    return _to_response(db_workout)

def get_all_workouts(db: Session) -> List[schemas.WorkoutResponse]:
    workouts = db.query(models.Workout).all()
    return [_to_response(w) for w in workouts]


def get_workouts_by_date(db: Session, target_date: date) \
        -> List[schemas.WorkoutResponse]:
    workouts = (
        db.query(models.Workout)
        .filter(models.Workout.workout_date == target_date)
        .all()
    )
    return [_to_response(w) for w in workouts]


def get_workout_by_id(db: Session, workout_id: int) -> models.Workout:
    return db.query(models.Workout).filter(models.Workout.id == workout_id).first()


def update_workout(db: Session, workout_id: int, workout_update: schemas.WorkoutUpdate):
    db_workout = get_workout_by_id(db, workout_id)
    if not db_workout:
        return None

    update_data = workout_update.model_dump(exclude_unset=True)

    # Если изменили тип — пересчитываем стоимость
    if "workout_type" in update_data:
        new_type = update_data["workout_type"]
        price = db_workout.client.price_per_session
        if new_type == "ПТ":
            update_data["total_cost"] = price
        elif new_type == "Сплит":
            update_data["total_cost"] = price * 0.75

    for field, value in update_data.items():
        setattr(db_workout, field, value)

    db.commit()
    db.refresh(db_workout)
    return _to_response(db_workout)

def delete_workout(db: Session, workout_id: int):
    db_workout = get_workout_by_id(db, workout_id)
    if not db_workout:
        return None
    response = _to_response(db_workout)
    db.delete(db_workout)
    db.commit()
    return response

# Вспомогательная функция: превращает ORM-объект в ответ с именем клиента
def _to_response(w: models.Workout) -> schemas.WorkoutResponse:
    return schemas.WorkoutResponse(
        id=w.id,
        client_id=w.client_id,
        client_name=w.client.name,
        workout_date=w.workout_date,
        workout_type=w.workout_type,
        total_cost=w.total_cost,
    )