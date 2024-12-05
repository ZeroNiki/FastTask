import sqlite3
from datetime import datetime

class TasksDB:
    def __init__(self, db_name="tasks.db") -> None:
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_table()


    def _create_table(self):
        create_user_table = """
        CREATE TABLE IF NOT EXISTS users (
                id INTENGER PRIMARY KEY,
                username TEXT
        );
        """

        create_tasks_table = """
        CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTENGER,
                task_name TEXT NOT NULL,
                description TEXT,
                date TEXT,
                is_done INTENGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id)
                ); 
        """

        self.cursor.execute(create_user_table)
        self.cursor.execute(create_tasks_table)
        self.connection.commit()

    def add_user(self, user_id, username):
        query = "INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)"
        self.cursor.execute(query, (user_id, username))
        self.connection.commit()

    def add_task(self, user_id, task_name, description=None, date=None):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        query = """
        INSERT INTO tasks (user_id, task_name, description, date, is_done) 
        VALUES (?, ?, ?, ?, 0);
        """

        self.cursor.execute(query)
        self.connection.commit()

    def get_user_task(self, user_id):
        query = "SELECT id, task_name, description, date, is_done FROM tasks WHERE user_id = ?;"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()

    def mark_task_done(self, task_id):
        query = "UPDATE tasks SET is_done = 1 WHERE id = ?;"
        self.cursor.execute(query)
        self.connection.commit()

    def close(self):
        self.connection.close()

