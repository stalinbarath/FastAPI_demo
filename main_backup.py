from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

#DB CONNECT

import psycopg2

conn = psycopg2.connect(
    database = 'demodb',
    user = 'postgres',
    password = 'admin',
    host = '127.0.0.1',
    port = 5432)

#CONFIG

import pandas as pd

config_data = pd.read_csv('/data/FastAPI_POC.csv')

'''
Steps:
1. Create a sample db and a model.
2. Create FastAPI instance.
3. a. Declare the api method with decorator
   b. Define a relevant function
'''

fakedb = []

class Course(BaseModel):
    id : int
    name : str
    price : float
    is_early_bird : Optional[bool] = None

app = FastAPI()

@app.get('/')
def read_root():
    '''Whatever datatypes we return (list,dict,string,etc.), FastAPI converts into json and displays in UI.'''
    cursor = conn.cursor()
    cursor.execute('select * from demotable')
    demodb_data = cursor.fetchall()
    return demodb_data

@app.get('/courses')
def get_courses():
    return fakedb

@app.get('/courses/{course_id}')
def get_course(course_id:int):
    return fakedb[course_id-1]

@app.post('/courses')
def add_course(course: Course):
    fakedb.append(course.dict())
    return fakedb[-1]

@app.delete('/course/{course_id}')
def delete_course(course_id:int):
    fakedb.pop(course_id-1)
    return {'task':'deletion successful'}
