import sqlite3

# create a connection with the database or create it , if it doesn't exist
connection = sqlite3.connect("database.db")

# create a cursor to control all the commands
cursor = connection.cursor()

# create the Table
cursor.execute(
    '''
    CREATE TABLE expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT;
    description TEXT,
    category TEXT,
    amount REAL,
    date TEXT
    )
    '''
)
# commit the changes
connection.commit()
# close the connection
connection.close()