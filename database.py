import sqlite3

DATABASE_NAME = "todorpg.db"

def get_connection():
    return sqlite3.connect(DATABASE_NAME)

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Tabelle für Nutzer
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            class TEXT NOT NULL,
            race TEXT NOT NULL,
            level INTEGER DEFAULT 0,
            xp INTEGER DEFAULT 0,
            max_xp INTEGER DEFAULT 100,
            dark_mode INTEGER DEFAULT 0
        )
    """)

    # Tabelle für Quests
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quest (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            difficulty TEXT NOT NULL,
            end_date TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

def user_exists():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM user")
    exists = cursor.fetchone()[0] > 0
    conn.close()
    return exists

def create_user(name, user_class, race):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user (name, class, race) VALUES (?, ?, ?)
    """, (name, user_class, race))
    conn.commit()
    conn.close()

def get_user():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user LIMIT 1")
    user = cursor.fetchone()
    conn.close()
    return user

def update_user_level_xp(level, xp, max_xp):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE user SET level = ?, xp = ?, max_xp = ? WHERE id = 1
    """, (level, xp, max_xp))
    conn.commit()
    conn.close()

def delete_user():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user")
    cursor.execute("DELETE FROM quest")
    conn.commit()
    conn.close()

def create_quest(name, description, difficulty, end_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO quest (name, description, difficulty, end_date) VALUES (?, ?, ?, ?)
    """, (name, description, difficulty, end_date))
    conn.commit()
    conn.close()

def get_quests():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quest WHERE completed = 0 ORDER BY id DESC")
    quests = cursor.fetchall()
    conn.close()
    return quests

def complete_quest(quest_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE quest SET completed = 1 WHERE id = ?
    """, (quest_id,))
    conn.commit()
    conn.close()

def update_dark_mode(is_dark: bool):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE user SET dark_mode = ? WHERE id = 1
    """, (1 if is_dark else 0,))
    conn.commit()
    conn.close()

def get_dark_mode() -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT dark_mode FROM user WHERE id = 1")
    result = cursor.fetchone()
    conn.close()
    return bool(result[0]) if result else False