import sqlite3
import pandas as pd
from datetime import datetime

DB_PATH = "crowd_system.db"

# ================== CONNECTION ==================
def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# ================== INIT DB ==================
def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS detections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        track_id INTEGER,
        x REAL,
        y REAL,
        timestamp TEXT
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS people_counter_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entered INTEGER,
        exited INTEGER,
        inside INTEGER,
        timestamp TEXT
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS system_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        level TEXT,
        message TEXT,
        timestamp TEXT
    )""")

    conn.commit()
    conn.close()

# ================== USERS ==================
def create_default_admin():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email='admin@admin.com'")
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users(email,password,role) VALUES (?,?,?)",
            ("admin@admin.com", "admin", "admin")
        )
        conn.commit()
    conn.close()

def add_user(email, password, role):
    try:
        conn = get_conn()
        conn.execute(
            "INSERT INTO users(email,password,role) VALUES (?,?,?)",
            (email, password, role)
        )
        conn.commit()
        conn.close()
        log("INFO", f"User created: {email}")
        return True
    except:
        return False

def validate_user(email, password):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT role FROM users WHERE email=? AND password=?",
        (email, password)
    )
    row = cur.fetchone()
    conn.close()
    return {"role": row[0], "email": email} if row else None

# ================== LOGGING ==================
def log(level, message):
    conn = get_conn()
    conn.execute(
        "INSERT INTO system_logs(level,message,timestamp) VALUES (?,?,?)",
        (level, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

# ================== DETECTIONS ==================
def save_detection(track_id, x, y):
    conn = get_conn()
    conn.execute(
        "INSERT INTO detections(track_id,x,y,timestamp) VALUES (?,?,?,?)",
        (int(track_id), float(x), float(y),
         datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

def get_detections():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT track_id, x, y, timestamp FROM detections ORDER BY timestamp ASC"
    )
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return pd.DataFrame(columns=["track_id", "x", "y", "timestamp"])

    return pd.DataFrame(rows, columns=["track_id", "x", "y", "timestamp"])

def get_counter_history():
    conn = get_conn()
    df = pd.read_sql(
        "SELECT entered, exited, inside, timestamp FROM people_counter_history ORDER BY timestamp",
        conn
    )
    conn.close()
    return df


# =================== ADD & Delete user Also show Log ================
def get_logs(limit=100):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT level, message, timestamp FROM system_logs ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = cur.fetchall()
    conn.close()

    return pd.DataFrame(rows, columns=["Level", "Message", "Timestamp"])

def delete_user(user_id):
    conn = get_conn()
    conn.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()

    log("INFO", f"User deleted (ID={user_id})")



# ================== COUNTER HISTORY ==================
def update_live_count(entered, exited, inside):
    conn = get_conn()
    conn.execute(
        "INSERT INTO people_counter_history(entered,exited,inside,timestamp) VALUES (?,?,?,?)",
        (entered, exited, inside,
         datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()
    
    

