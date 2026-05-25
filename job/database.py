# database.py

import psycopg2

conn = psycopg2.connect(

    host="localhost",

    database="jobdb",

    user="postgres",

    password="sql@123"

)

cursor = conn.cursor()

# =========================
# CREATE TABLE IF NOT EXISTS
# =========================

cursor.execute("""

CREATE TABLE IF NOT EXISTS users (

    id SERIAL PRIMARY KEY,

    name VARCHAR(100),

    education VARCHAR(100),

    skills TEXT,

    interests TEXT,

    domains TEXT,

    recommended_career VARCHAR(200),

    match_score FLOAT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")

conn.commit()