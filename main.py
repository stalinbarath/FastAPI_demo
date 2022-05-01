from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from settings import conn,config_data

from schemas import schemas
from models import models
from db.session import Base, SessionLocal, engine

#Creates a table in the 'database' with schema defined in models->models.py
#Created only if the table isn't present.
models.Base.metadata.create_all(engine)

app = FastAPI()
cursor = conn.cursor()

@app.get('/single_iteration')
def fetch_data(iteration:int):

    #1. Get config data
    iter_data = config_data.loc[config_data['iteration'] == iteration]
    iter_id = iter_data['iteration'].item()
    iter_table = iter_data['table_name'].item()
    iter_col = iter_data['column'].item()
    iter_val = iter_data['value'].item()
    
    #2. Get table data and column names
    if type(iter_val)==str:
        cursor.execute('select * from '+ iter_table + ' where '+ iter_col + ' = %s',[iter_val])
    else:
        cursor.execute('select * from '+ iter_table + ' where '+ iter_col + str(iter_val))
    iter_db_data = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description] 

    #3. Combine data and columns as dict
    fetch_result = {}
    all_result = {}

    if len(iter_db_data) > 1:
        for iter in range(0,len(iter_db_data)):
            iter_db_data_list = list(iter_db_data[iter])
            for i in range(0,len(colnames)):
                fetch_result[colnames[i]] = iter_db_data_list[i]
            all_result[iter] = fetch_result.copy()
    else:
        iter_db_data_list = list(iter_db_data[0])
        for i in range(0,len(colnames)):
            all_result[colnames[i]] = iter_db_data_list[i]

    return {iter_id:{'table':iter_table,'result':all_result}}

@app.get('/all_iteration')
def get_data():

    all_data = {}
    cursor = conn.cursor()

    for iteration in range(1, config_data.shape[0]+1):

        #1. Get config data
        iter_data = config_data.loc[config_data['iteration'] == iteration]
        iter_id = iter_data['iteration'].item()
        iter_table = iter_data['table_name'].item()
        iter_col = iter_data['column'].item()
        iter_val = iter_data['value'].item()

        #2. Get table data and column names
        if type(iter_val)==str:
            cursor.execute('select * from '+ iter_table + ' where '+ iter_col + ' = %s',[iter_val])
        else:
            cursor.execute('select * from '+ iter_table + ' where '+ iter_col + str(iter_val))
        iter_db_data = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description] 
        
        #3. Combine data and columns as dict
        fetch_result = {}
        all_result = {}

        if len(iter_db_data) > 1:
            for iter in range(0,len(iter_db_data)):
                iter_db_data_list = list(iter_db_data[iter])
                for i in range(0,len(colnames)):
                    fetch_result[colnames[i]] = iter_db_data_list[i]
                all_result[iter] = fetch_result.copy()
        else:
            iter_db_data_list = list(iter_db_data[0])
            for i in range(0,len(colnames)):
                all_result[colnames[i]] = iter_db_data_list[i]

        all_data.update({iter_id:{'table':iter_table,'result':all_result}})

    return all_data

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/Add_Profile')
def create_profile(profile: schemas.Profile, db: Session = Depends(get_db)):
    new_profile = models.Profile(id = profile.id, name = profile.name, age = profile.age)
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

@app.get('/Get_Profile')
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    return profile

@app.delete('/Delete_Profile')
def del_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(models.Profile2).filter(models.Profile2.id == profile_id).delete(synchronize_session=False)
    db.commit()
    return "done"