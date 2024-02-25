from fastapi import FastAPI
from . import models
from .database import engine
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .routers import post, user, health_check

models.Base.metadata.create_all(bind=engine)


# server instance
app = FastAPI()

# database connection
while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi-tuts", user="postgres", password="postgres", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as error:
        print(f"Error connecting to database\n{error}")
        time.sleep(2)

# add routes from the router directory
app.include_router(post.router)
app.include_router(user.router)
app.include_router(health_check.router)