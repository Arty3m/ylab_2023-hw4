from sqlalchemy.ext.asyncio import AsyncSession


class ServiceMixin:
    def __init__(self, db: AsyncSession, cache):
        self.db: AsyncSession = db
        self.cache = cache
