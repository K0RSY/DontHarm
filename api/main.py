from fastapi import *
from models import *
from sqlalchemy import *
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from fastapi.security import OAuth2PasswordRequestForm
import json
from token_part import *

app = FastAPI()

def convert_table_name(name: str):
    name_parts = name.split("_")
    result = ""

    for name_part in name_parts:
        result += f"{name_part[0].upper()}{name_part[1:].lower()}"

    return result

@app.post("/token", response_model=Token)
def login_for_access_token(data: UserModel, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.login, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Login or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(data={"sub": user.login})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/get_field/{table}/{return_field}/{find_field}/{find_value}")
def get_field(table: str, return_field: str, find_field: str, find_value: str, db: Session = Depends(get_db), current_user: LaboratoryAssistants = Depends(get_current_user)):
    if not current_user:
        return None
    table_class = eval(convert_table_name(table))
    find_field_var = eval(f"table_class.{find_field}")
    return eval(f"db.query(table_class).filter(find_field_var == find_value).first().{return_field}")

@app.get("/get_row/{table}/{find_field}/{find_value}")
def get_row(table: str, find_field: str, find_value: str, db: Session = Depends(get_db), current_user: LaboratoryAssistants = Depends(get_current_user)):
    if not current_user:
        return None
    table_class = eval(convert_table_name(table))
    find_field_var = eval(f"table_class.{find_field}")
    return db.query(table_class).filter(find_field_var == find_value).first()

@app.get("/get_column/{table}/{return_field}")
def get_column(table: str, return_field: str, db: Session = Depends(get_db), current_user: LaboratoryAssistants = Depends(get_current_user)):
    if not current_user:
        return None
    table_class = eval(convert_table_name(table))
    result = []
    for table_instance in db.query(table_class).all():
        result.append(eval(f"table_instance.{return_field}"))

    return result

@app.get("/get_all/{table}")
def get_all(table: str, db: Session = Depends(get_db), current_user: LaboratoryAssistants = Depends(get_current_user)):
    if not current_user:
        return None
    table_class = eval(convert_table_name(table))
    return db.query(table_class).all()

@app.post("/submit_fields/{table}")
def submit_fields(table: str, data = Body(), db: Session = Depends(get_db), current_user: LaboratoryAssistants = Depends(get_current_user)):
    if not current_user:
        return None
    table_class = eval(convert_table_name(table))
    data_instance_string = ", ".join([f"{key}=data['{key}']" for key in data.keys()])
    data_instance = eval(f"table_class({data_instance_string})")

    db.add(data_instance)
    db.commit()
    db.refresh(data_instance)
    
    return data_instance
    
@app.put("/edit_fields/{table}/{find_field}/{find_value}")
def edit_fields(table: str, find_field: str, find_value: str, data = Body(), db: Session = Depends(get_db), current_user: LaboratoryAssistants = Depends(get_current_user)):
    if not current_user:
        return None
    table_class = eval(convert_table_name(table))
    find_field_var = eval(f"table_class.{find_field}")
    data_instance = db.query(table_class).filter(find_field_var == find_value).first()

    for key in data.keys():
        exec(f"data_instance.{key} = data['{key}']")

    db.commit()
    db.refresh(data_instance)

    return data_instance

@app.delete("/remove_row/{table}/{find_field}/{find_value}")
def remove_row(table: str, find_field: str, find_value: str, db: Session = Depends(get_db), current_user: LaboratoryAssistants = Depends(get_current_user)):
    if not current_user:
        return None
    table_class = eval(convert_table_name(table))
    find_field_var = eval(f"table_class.{find_field}")
    data_instance = db.query(table_class).filter(find_field_var == find_value).first()

    if data_instance == None:
        return responses.JSONResponse( status_code=404, content={ "message": "Пользователь не найден"})
    
    db.delete(data_instance)
    db.commit()
    
    return data_instance

@app.get("/get_current_user")
def read_LaboratoryAssistants_me(current_user: LaboratoryAssistants = Depends(get_current_user)):
    return current_user