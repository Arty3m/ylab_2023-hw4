from sqlmodel import Session


# from src.db import

class ServiceMixin:
    def __init__(self, db: Session):
        self.db: Session = db
