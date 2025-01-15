# kubernetes exam
Create a pod with replicas with a FastAPI server communicating with MySQL including secrets and ingress.<br><br>
This environment can serve as a base for other projects requiring a pod with FastAPI and MySQL.
DB data and FAPI endpoints will just need to be added (and previous ones deleted of course).


## Presentation
This evaluation will consist of creating a set of commented deployment files designed to deploy a data API. Our API consists of two containers:

the first contains a MySQL database: datascientest/mysql-k8s:1.0.0.
the second contains a FastAPI API
The FastAPI API container has not yet been built, but the various files have already been created:

The Dockerfile:
```
FROM ubuntu:20.04

ADD files/requirements.txt files/main.py ./

RUN apt update && apt install python3-pip libmysqlclient-dev -y && pip install -r requirements.txt

EXPOSE 8000

CMD uvicorn main:server --host 0.0.0.0
```

The main.py file containing the API:
```
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.engine import create_engine

# creating a FastAPI server
server = FastAPI(title='User API')

# creating a connection to the database
mysql_url = '' # to complete
mysql_user = 'root
mysql_password = '' # to complete
database_name = 'Main'

# recreating the URL connection
connection_url = 'mysql://{user}:{password}@{url}/{database}'.format(
    user=mysql_user,
    password=mysql_password,
    url=mysql_url,
    database=database_name
)

# creating the connection
mysql_engine = create_engine(connection_url)


# creating a User class
class User(BaseModel):
    user_id: int = 0
    username: str = 'daniel
    email: str = 'daniel@datascientest.com'


@server.get('/status')
async def get_status():
    """Returns 1
    """
    return 1


@server.get('/users')
async def get_users():
    with mysql_engine.connect() as connection:
        results = connection.execute('SELECT * FROM Users;')

    results = [
        User(
            user_id=i[0],
            username=i[1],
            email=i[2]
            ) for i in results.fetchall()]
    return results


@server.get('/users/{user_id:int}', response_model=User)
async def get_user(user_id):
    with mysql_engine.connect() as connection:
        results = connection.execute(
            'SELECT * FROM Users WHERE Users.id = {};'.format(user_id))

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
```

The requirements.txt file, which contains the Python libraries to be installed:
```
fastapi
sqlalchemy
mysqlclient==2.1.1
uvicorn
```

## Instructions
The aim of this exercise is to create a Deployment with 3 Pods, each containing both a MySQL container and a FastAPI container. We'll then need to create a Service and an Ingress to enable access to the API.

We will therefore need to complete the code provided for the API and rebuild the corresponding Docker image (and upload it to DockerHub), so as to enable communication between the API and the database. In addition, you'll need to change the API code to retrieve the database password: datascientest1234. However, this password cannot be hard-coded and must therefore be put in a Secret.

## Renderings
The expected output is a set of files, with a comment file if required:

- the reworked main.py file
- a my-deployment-eval.yml file containing the Deployment declaration
- a my-service-eval.yml file containing the Service declaration
- a my-ingress-eval.yml file containing the Ingress declaration
- a my-secret-eval.yml file containing the Secret declaration

## Solution
Several errors have been encountered forcing to modify the main.py a lot more than necessary.
The most annoying error was this one, which in fact hid several issues. The most important one being an issue with the DBAPI :<br>
`sqlalchemy.exc.OperationalError: (MySQLdb.OperationalError) (2002, "Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)")`<br>
Hence, I modified the connection method to the database so SQLAlchemy uses the pymysql library to connect to MySQL.

**For the installation to work you have to use the code in main_sqlalchemy.py for your main.py file. The Kubernetes deployment file is modified already. It uses a different docker image.**

For the rest, it's all quite straightforward. System environment vars, secret for the root password, etc.<br>
Enjoy!

