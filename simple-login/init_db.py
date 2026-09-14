from database import get_db

db = get_db()

db.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

users = [
    ("admin", "admin123"),
    ("user1", "password123"),
    ("user2", "123456")
]

for username, password in users:
    db.execute(
        "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )

db.commit()
db.close()

print("Database initialized.")
