from getpass import getpass

from app.database.connection import SessionLocal
from app.models.user import User
from app.core.security import hash_password


username = input("Enter admin username: ")
email = input("Enter admin email: ")
password = getpass("Enter admin password: ")


db = SessionLocal()

try:
    existing_admin = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if existing_admin:
        print("Admin username already exists.")
    else:
        admin = User(
            username=username,
            email=email,
            hashed_password=hash_password(password),
            role="admin"
        )

        db.add(admin)
        db.commit()

        print("Admin user created successfully.")

finally:
    db.close()