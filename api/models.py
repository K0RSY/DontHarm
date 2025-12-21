from typing import Optional

from sqlalchemy import BINARY, Date, Integer, String, Double, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime
from pydantic import BaseModel

class UserModel(BaseModel):
    login: str
    password: str
        
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    login: str

class Base(DeclarativeBase):
    pass

class LaboratoryAssistants(Base):
    __tablename__ = 'laboratory_assistants'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    login: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(100))
    surname: Mapped[Optional[str]] = mapped_column(String(100))
    name: Mapped[Optional[str]] = mapped_column(String(100))
    patronymic: Mapped[Optional[str]] = mapped_column(String(100))
    lastEnterDateTime: Mapped[datetime.date] = mapped_column(Date)

class Clients(Base):
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    login: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(100))
    surname: Mapped[Optional[str]] = mapped_column(String(100))
    name: Mapped[Optional[str]] = mapped_column(String(100))
    patronymic: Mapped[Optional[str]] = mapped_column(String(100))
    dateOfBirth: Mapped[Optional[str]] = mapped_column(Date())
    passportSeria: Mapped[Optional[str]] = mapped_column(String(100))
    passportNumber: Mapped[Optional[str]] = mapped_column(String(100))
    phone: Mapped[Optional[str]] = mapped_column(String(100))
    email: Mapped[Optional[str]] = mapped_column(String(100))
    
class Services(Base):
    __tablename__ = 'services'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(100))
    
class Orders(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    serviceId: Mapped[int] = mapped_column(Integer)
    clientId: Mapped[int] = mapped_column(Integer)