CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    student_email TEXT NOT NULL,
    total_marks INTEGER NOT NULL,
    obtained_marks INTEGER NOT NULL,
    percentage REAL NOT NULL,
    status TEXT NOT NULL,
    responses TEXT NOT NULL,
    submitted_at TEXT DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS meetup_registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    whatsapp_number TEXT NOT NULL,
    working_on TEXT NOT NULL,
    role TEXT NOT NULL,
    looking_for TEXT NOT NULL,
    attendance TEXT NOT NULL,
    biggest_problem TEXT
);
