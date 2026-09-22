import sqlite3


def get_connection():
    connection = sqlite3.connect("tasks.db")
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
        """
    )
    connection.commit()
    return connection
