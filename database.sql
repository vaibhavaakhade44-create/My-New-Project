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

-- Practice: insert one meetup registration.
-- INSERT INTO meetup_registrations (
--     full_name, whatsapp_number, working_on, role, looking_for, attendance, biggest_problem
-- ) VALUES (
--     'Hariom Singh', '9876543210', 'Building an AI Resume Screener',
--     'Founder', 'Funding', 'Yes', 'Marketing and user acquisition'
-- );

-- Practice: list all registrations.
-- SELECT * FROM meetup_registrations;

-- Practice: find one person by name.
-- SELECT * FROM meetup_registrations WHERE full_name = 'Hariom Singh';

-- Practice: count people who plan to attend.
-- SELECT COUNT(*) FROM meetup_registrations WHERE attendance = 'Yes';