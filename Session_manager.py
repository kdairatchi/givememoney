# session_manager.py
import sqlite3
from datetime import datetime

def init_db():
    """Initializes the session database if it doesn't exist."""
    conn = sqlite3.connect('session.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS sessions
                      (id INTEGER PRIMARY KEY, session_name TEXT, domain TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS scan_results
                      (id INTEGER PRIMARY KEY, session_id INTEGER, tool_name TEXT, results TEXT, scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    return conn

def create_new_session(session_name, domain):
    """Create a new session for the user."""
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sessions (session_name, domain) VALUES (?, ?)", (session_name, domain))
    conn.commit()
    return cursor.lastrowid

def save_scan_results(session_id, tool_name, results_file):
    """Save scan results to the session."""
    conn = init_db()
    cursor = conn.cursor()
    with open(results_file, 'r') as f:
        results = f.read()
    cursor.execute("INSERT INTO scan_results (session_id, tool_name, results) VALUES (?, ?, ?)", (session_id, tool_name, results))
    conn.commit()

def load_sessions():
    """Load all saved sessions."""
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions")
    return cursor.fetchall()

def load_scan_results(session_id):
    """Load scan results for a session."""
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scan_results WHERE session_id = ?", (session_id,))
    return cursor.fetchall()
