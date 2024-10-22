# database.py

import sqlite3

def create_connection():
    conn = sqlite3.connect('todrpg.db')
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    # Tabelle für Aufgaben erstellen (inkl. neue Attribute)
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

    # Tabelle für Benutzer erstellen (inkl. coins)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
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
    cursor.execute('INSERT INTO users (username, level, xp, coins) VALUES (?, ?, ?, ?)',
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

def get_users():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users
