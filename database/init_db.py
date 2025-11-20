from sqlalchemy.orm import Session

from database.session import engine, Base, SessionLocal
from models.user import User
from models import account, attachment, security_log, token_session  # noqa: F401
from security.hashing import get_password_hash


def init_db():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        if not db.query(User).filter(User.email == "admin@local").first():
            admin = User(
                email="admin@local",
                full_name="Administrator",
                role="admin",
                hashed_password=get_password_hash("ChangeMe123!"),
                master_password_hash=get_password_hash("ChangeMe123!"),
            )
            db.add(admin)
            db.commit()


if __name__ == "__main__":
    init_db()
