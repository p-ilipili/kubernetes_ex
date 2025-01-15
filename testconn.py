echo "from sqlalchemy import create_engine

# Connection details
mysql_url = 'localhost'  # Since MySQL is in the same pod
mysql_user = 'root'
mysql_password = 'datascientest1234'
database_name = 'Main'

# Connection string
connection_url = 'mysql://{user}:{password}@{url}/{database}'.format(
    user=mysql_user,
    password=mysql_password,
    url=mysql_url,
    database=database_name
)

# Create the engine
engine = create_engine(connection_url)

# Test the connection
try:
    with engine.connect() as connection:
        result = connection.execute('SHOW TABLES;')  # Query to list all tables
        print('Connection successful! Tables:', result.fetchall())
except Exception as e:
    print('Connection failed:', str(e))
" > test_connection.py