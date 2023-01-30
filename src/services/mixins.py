from sqlmodel import Session


class ServiceMixin:
    def __init__(self, db: Session, cache):
        self.db: Session = db
        self.cache = cache
