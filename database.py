"""
DevQuest - SQLite Database Module
=================================
This file handles all SQLite database operations for quiz submissions.
Can be imported in app.py OR run directly in terminal via:
    python database.py
"""

import sqlite3
import json
import os
import sys

# Windows terminal UTF-8 encoding support
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'quiz.db')

def get_connection():
    """Returns a connection to the SQLite database with row_factory configured."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database table if it doesn't already exist."""
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                student_email TEXT NOT NULL,
                total_marks INTEGER NOT NULL,
                obtained_marks INTEGER NOT NULL,
                percentage REAL NOT NULL,
                status TEXT NOT NULL,
                responses TEXT NOT NULL,
                submitted_at TEXT DEFAULT (datetime('now','localtime'))
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS meetup_registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                whatsapp_number TEXT NOT NULL,
                working_on TEXT NOT NULL,
                role TEXT NOT NULL,
                looking_for TEXT NOT NULL,
                attendance TEXT NOT NULL,
                biggest_problem TEXT
            )
        ''')
        conn.commit()
    return True

def save_submission(name, email, total_marks, obtained_marks, percentage, status, responses):
    """
    Saves a new quiz submission into the database.
    
    :param name: Candidate's full name
    :param email: Candidate's email
    :param total_marks: Total possible marks
    :param obtained_marks: Marks scored
    :param percentage: Percentage scored
    :param status: Pass / Fail status
    :param responses: List or dict of question-by-question responses (stored as JSON)
    :return: id of the inserted submission
    """
    init_db()
    responses_json = json.dumps(responses) if not isinstance(responses, str) else responses
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO submissions 
               (student_name, student_email, total_marks, obtained_marks, percentage, status, responses) 
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (name, email, total_marks, obtained_marks, percentage, status, responses_json)
        )
        conn.commit()
        return cursor.lastrowid

def get_all_submissions():
    """Fetches all submissions sorted by latest first."""
    init_db()
    with get_connection() as conn:
        rows = conn.execute('SELECT * FROM submissions ORDER BY submitted_at DESC').fetchall()
        return [dict(r) for r in rows]

def get_submission_by_id(submission_id):
    """Fetches a single submission by its ID."""
    init_db()
    with get_connection() as conn:
        row = conn.execute('SELECT * FROM submissions WHERE id = ?', (submission_id,)).fetchone()
        return dict(row) if row else None

def get_stats():
    """Calculates overall statistics for all candidates."""
    submissions = get_all_submissions()
    total = len(submissions)
    passed = sum(1 for s in submissions if 'Pass' in s.get('status', ''))
    avg_score = round(sum(s.get('obtained_marks', 0) for s in submissions) / max(1, total), 1)
    pass_pct = round((passed / max(1, total)) * 100, 1)
    return {
        "total_submissions": total,
        "passed_count": passed,
        "average_score": avg_score,
        "pass_rate_percentage": pass_pct
    }

def print_table():
    """Prints all submissions in a clean ASCII table in the console."""
    submissions = get_all_submissions()
    stats = get_stats()

    print("\n" + "=" * 90)
    print("                DATABASE RECORDS: quiz.db (Table: submissions)                ")
    print("=" * 90)

    if not submissions:
        print("  No records found in database yet.")
    else:
        header = f"{'ID':<4} | {'Name':<22} | {'Email':<28} | {'Score':<8} | {'%':<6} | {'Status':<16} | {'Date & Time'}"
        print(header)
        print("-" * 90)
        for s in submissions:
            score_str = f"{s['obtained_marks']}/{s['total_marks']}"
            pct_str = f"{s['percentage']}%"
            # Strip non-ascii if needed for older windows terminals
            status_clean = s['status'].encode('ascii', 'ignore').decode('ascii').strip() or s['status']
            row = f"{s['id']:<4} | {s['student_name'][:22]:<22} | {s['student_email'][:28]:<28} | {score_str:<8} | {pct_str:<6} | {status_clean:<16} | {s['submitted_at']}"
            print(row)

    print("-" * 90)
    print(f"Stats: Total = {stats['total_submissions']} | Passed = {stats['passed_count']} | Average Score = {stats['average_score']} pts | Pass Rate = {stats['pass_rate_percentage']}%")
    print("=" * 90 + "\n")

if __name__ == '__main__':
    # Initialize DB if not created
    init_db()
    print_table()
