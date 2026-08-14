CREATE TABLE IF NOT EXISTS internships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT,
    eligibility_criteria TEXT,
    ctc TEXT,
    stipend TEXT,
    last_date TEXT,
    role TEXT,
    location TEXT,
    process_details TEXT,
    is_eligible BOOLEAN,
    rejection_reason TEXT,
    email_id TEXT UNIQUE,
    date_received DATETIME DEFAULT CURRENT_TIMESTAMP
);
