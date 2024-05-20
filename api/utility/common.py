from ..db.database import SessionLocal


# db Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
