from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
import os

# creating a FastAPI server
server = FastAPI(title='User API')

# retrieving database credentials from environment variables
mysql_url = os.getenv('MYSQL_URL', 'localhost:3306')
mysql_user = os.getenv('MYSQL_USER', 'root')
mysql_password = os.getenv('MYSQL_PASSWORD', '')
database_name = os.getenv('DATABASE_NAME', 'Main')

# Connection URL using pymysql
connection_url = 'mysql+pymysql://{user}:{password}@{url}/{database}'.format(
    user=mysql_user,
    password=mysql_password,
    url=mysql_url,
    database=database_name
)

# Create SQLAlchemy engine
mysql_engine = create_engine(connection_url, pool_pre_ping=True)

# Create a sessionmaker bound to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=mysql_engine)

# Create a base class for models
Base = declarative_base()

# Create a User class model (SQLAlchemy model)
class User(BaseModel):
    user_id: int
    username: str
    email: str

# Initialize FastAPI server
server = FastAPI()

# Health check route
@server.get('/status')
async def get_status():
    """Returns 1"""
    return 1

# Route to get all users
@server.get('/users')
async def get_users():
    try:
        # Create a session using SessionLocal
        db = SessionLocal()
        results = db.execute(text('SELECT * FROM Users;'))

        # Map the query results to User objects
        users = [
            User(
                user_id=i[0],
                username=i[1],
                email=i[2]
            ) for i in results.fetchall()]
        db.close()
        return users
    except Exception as e:
        db.close()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Route to get a specific user by user_id
@server.get('/users/{user_id:int}', response_model=User)
async def get_user(user_id: int):
    try:
        db = SessionLocal()
        query = text('SELECT * FROM Users WHERE Users.id = :user_id')
        results = db.execute(query, {'user_id': user_id})

        # Map the query results to User objects
        users = [
            User(
                user_id=i[0],
                username=i[1],
                email=i[2]
            ) for i in results.fetchall()]

        db.close()

        if len(users) == 0:
            raise HTTPException(
                status_code=404,
                detail='Unknown User ID'
            )
        return users[0]
    except Exception as e:
        db.close()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")