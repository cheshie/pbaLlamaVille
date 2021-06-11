from sqlalchemy.orm import Session,contains_eager
from sqlalchemy import and_, cast, DateTime
import model
import schemas
from random import randint
from datetime import datetime
from passlib.hash import bcrypt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


SECRET_KEY = "4c793ed1fa15761c79a777757ce452fcd7ecc8c0d0f0116c943908f466181424"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 2
xjwssig_pass = "secret123456"

class User:
    username = 'llamaoperator'
    password = '$2b$13$eu5qZT4dM1p6bEyMCVc.tu4GpZ2TGfEwGdkhKKYk.9yApHq9pSMem'

def authenticate_user(form: OAuth2PasswordRequestForm):
    if  bcrypt.verify(form.password , User.password) and form.username == User.username:
        return True
    return False
#

def get_llama(db: Session, llama_id: int):
    return db.query(model.Llama).filter(model.Llama.id == llama_id).first()

def get_llamas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Llama).offset(skip).limit(limit).all()

def create_llama(db: Session, llama: schemas.Llama):
    try: 
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
    except Exception:
        return False
    return True

def update_llama(db: Session, llama: schemas.Llama, id: int):
    try:
        llama_db = db.query(model.Llama).filter(model.Llama.id == id).update(
            {
                model.Llama.name : llama.name,
                model.Llama.age : llama.age,
                model.Llama.breed : llama.breed.value,
                model.Llama.coat : llama.coat,
                model.Llama.color : llama.color
            }
        )
    
        db.commit()
        return True
    except Exception:
        return False
    #

def delete_llama(db: Session, llamaId: int):
    try:
        db.query(model.Llama).filter(model.Llama.id == llamaId).delete()
        db.commit()
    except Exception:
        return False
    return True
#

def get_schedules(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Schedule).offset(skip).limit(limit).all()

def create_schedule(db: Session, schedule: schemas.Schedule):
    db_schedule = model.Schedule(
        id = randint(0, 1000000),
        assignee_id = schedule.assignee_id,
        beginDate = schedule.beginDate,
        endDate = schedule.endDate
    )
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

# Get all llamas where schedtime is between their start and end of schedule
def get_llamas_at_schedule(db: Session, schedtime: datetime, skip: int = 0, limit: int = 100):
    return db.query(model.Llama).join(model.Llama.schedule).filter(and_(model.Schedule.beginDate <= schedtime, 
            model.Schedule.endDate >= schedtime)).all()