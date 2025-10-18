import sqlite3


def creates_tables():
    # create a connection with the database or create it , if it doesn't exist
    connection = sqlite3.connect("database.db")

    # create a cursor to control all the commands
    cursor = connection.cursor()

    # create the Table
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL
            )
        ''')
    # commit the changes
    connection.commit()
    # close the connection
    connection.close()
    print("Database and table created (if not exists).")


def add_expense(description, category, amount, date):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO expenses (description, category, amount, date) VALUES (?, ?, ?, ?)",
                   (description, category, amount, date)
                   )
    connection.commit()
    connection.close()


def get_expense():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    connection.close()
    return rows


def delete_expense(expense_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM expenses WHERE id= ?", (expense_id,))
    connection.commit()
    connection.close()


if __name__ == "__main__":
    creates_tables()
