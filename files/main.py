from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text
import os

# creating a FastAPI server
server = FastAPI(title='User API')

# retrieving database credentials from environment variables
mysql_url = os.getenv('MYSQL_URL', 'localhost:3306')
mysql_user = os.getenv('MYSQL_USER', 'root')
mysql_password = os.getenv('MYSQL_PASSWORD', '')
database_name = os.getenv('DATABASE_NAME', 'Main')

# recreating the URL connection
connection_url = 'mysql://{user}:{password}@{url}/{database}'.format(
    user=mysql_user,
    password=mysql_password,
    url=mysql_url,
    database=database_name
)

# creating the connection
mysql_engine = create_engine(connection_url,pool_pre_ping=True)


# creating a User class
class User(BaseModel):
    user_id: int = 0
    username: str = 'daniel'
    email: str = 'daniel@datascientest.com'


@server.get('/status')
async def get_status():
    """Returns 1
    """
    return 1


@server.get('/users')
async def get_users():
    try:
        with mysql_engine.connect() as connection:
            results = connection.execute(text('SELECT * FROM Users;'))

        results = [
            User(
                user_id=i[0],
                username=i[1],
                email=i[2]
            ) for i in results.fetchall()]
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@server.get('/users/{user_id:int}', response_model=User)
async def get_user(user_id):
    query = text('SELECT * FROM Users WHERE Users.id = :user_id')
    with mysql_engine.connect() as connection:
        results = connection.execute(query, {'user_id': user_id})

    results = [
        User(
            user_id=i[0],
            username=i[1],
            email=i[2]
        ) for i in results.fetchall()]

    if len(results) == 0:
        raise HTTPException(
            status_code=404,
            detail='Unknown User ID')
    else:
        return results[0]