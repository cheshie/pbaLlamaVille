from sqlalchemy.orm import Session
import model
import schemas
from random import randint


def get_llama(db: Session, llama_id: int):
    return db.query(model.Llama).filter(model.Llama.id == llama_id).first()

def get_llamas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Llama).offset(skip).limit(limit).all()

def create_llama(db: Session, llama: schemas.Llama):
    db_llama = model.Llama(
                    id=randint(0, 1000000),
                    name=llama.name,
                    age=llama.age,
                    breed=llama.breed.value,
                    color=llama.color,
                    coat=llama.coat,
            )
    
    db.add(db_llama)
    db.commit()
    db.refresh(db_llama)
    return db_llama

def update_llama(db: Session, llama: schemas.Llama):
    llama_db = db.query(model.Llama).filter(model.Llama.id == llama.id).first()
    # How to implement update?
    if llama_db:
        pass

def delete_llama(db: Session, llamaId: int):
    return db.delete(db.query(model.Llama).filter(model.Llama.id == llama_id).first())
#

def get_schedules(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Schedule).offset(skip).limit(limit).all()

def create_schedule(db: Session, schedule: schemas.Schedule, llama_id: int):
    db_schedule = model.Schedule(**schedule.dict(), owner_id=llama_id)
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule