from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price_per_session = Column(Float, nullable=False)
    package_balance = Column(Float, default=0)  # остаток баланса в пакете

    workouts = relationship("Workout", back_populates="client")

class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    workout_type = Column(String, nullable=False)
    workout_date = Column(Date, nullable=False)
    total_cost = Column(Float, nullable=False)

    client = relationship("Client", back_populates="workouts")