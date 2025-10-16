from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from typing import Optional, List
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth


#  This line tells SQLAlchemy to create all tables defined in your models.py
# It uses the engine (which knows your database connection URL)
# So basically: "Sync my Python models with the actual database tables"
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:

    try:
        conn = psycopg2.connect(host="localhost",
                                database="fastapi",
                                 user="postgres",
                                password="password1234",
                                cursor_factory =RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("connecting to database has failed")
        print("Error:  ", error)
        # the line below just tries connecting even when there is no internet access, wrong password etc
        time.sleep(4)
my_posts = [{"title": "title of post", "content": "content of post 1", "id": 1},
           {"title": "favorite foods", "content": "I like Pizza", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return id


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


app.include_router(post.router)
app.include_router(auth.router)
app.include_router(user.router)


@app.get("/")
def read_root():
    return {"message": "welcome to my api  ????"}


