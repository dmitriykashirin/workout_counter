from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from typing import Optional, List


# --- Клиенты ---

class ClientCreate(BaseModel):
    name: str = Field(..., min_length=2, description="Имя клиента")
    price_per_session: float = Field(..., gt=0, description="Цена одной персональной тренировки")
    package_balance: float = Field(0, ge=0, description="Остаток баланса в пакете")


class ClientUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    price_per_session: Optional[float] = Field(None, gt=0)
    package_balance: Optional[float] = Field(None, ge=0)


class ClientResponse(BaseModel):
    id: int
    name: str
    price_per_session: float
    package_balance: float
    model_config = ConfigDict(from_attributes=True)


# --- Тренировки ---

class WorkoutCreate(BaseModel):
    client_id: int = Field(..., description="ID клиента")
    workout_date: date = Field(..., description="Дата тренировки YYYY-MM-DD")
    workout_type: str = Field(..., description="ПТ или Сплит")


class WorkoutUpdate(BaseModel):
    workout_date: Optional[date] = Field(None)
    workout_type: Optional[str] = Field(None)


class WorkoutResponse(BaseModel):
    id: int
    client_id: int
    client_name: str
    workout_date: date
    workout_type: str
    total_cost: float
    model_config = ConfigDict(from_attributes=True)




