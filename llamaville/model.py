from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base
from schemas import Breed

class Llama(Base):
    __tablename__ = "llamas"

    id   = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age  = Column(Integer)
    breed= Column(String)
    color= Column(String)
    coat = Column(String)

    schedule = relationship("Schedule", back_populates="assignee")


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    assignee_id = Column(Integer, ForeignKey("llamas.id"))
    beginDate = Column(DateTime)
    endDate   = Column(DateTime)
    

    assignee = relationship("Llama", back_populates="schedule")