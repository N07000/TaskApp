# database.py

import sqlite3

def create_connection():
    conn = sqlite3.connect('todrpg.db')
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    # Tabelle für Aufgaben erstellen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            taskname TEXT,
            taskdesc TEXT,
            difficulty TEXT,
            status TEXT,
            priority TEXT,
            finaldate TEXT
        )
    ''')

    # Tabelle für User erstellen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            level INTEGER,
            xp INTEGER,
            coins INTEGER
        )
    ''')

    conn.commit()
    conn.close()

def save_task(task):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (taskname, taskdesc, difficulty, status, priority, finaldate) VALUES (?, ?, ?, ?, ?, ?)',
                   (task.taskname, task.taskdesc, task.difficulty, task.status, task.priority, task.finaldate))
    conn.commit()
    conn.close()

def save_user(user):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO user (username, level, xp, coins) VALUES (?, ?, ?, ?)',
                   (user.username, user.level, user.xp, user.coins))
    conn.commit()
    conn.close()

def get_tasks():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def load_user():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user LIMIT 1')
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        return User(username=user_data[1], level=user_data[2], xp=user_data[3], coins=user_data[4])
    return None
