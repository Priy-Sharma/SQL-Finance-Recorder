import pymysql

hostname = 'localhost'
user = 'root'
password = 'Root@123'

# Initializing connection
db = pymysql.connections.Connection(
    host=hostname,
    user=user,
    password=password
)

# Creating cursor object
cursor = db.cursor()

# Executing SQL query
cursor.execute("CREATE DATABASE IF NOT EXISTS finance_db")
cursor.execute("SHOW DATABASES")

# Displaying databases
for databases in cursor:
    print(databases)

# Closing the cursor and connection to the database
cursor.close()
db.close()