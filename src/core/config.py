import os

VERSION: str = "1.0.0"

# Название проекта. Используется в Swagger-документации
PROJECT_NAME: str = os.getenv("PROJECT_NAME", "ylab_2023_hw3")
BASEDIR: str = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
)
# Настройки Postgres
POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_DB: str = os.getenv("POSTGRES_DB", "ylab_hw")
POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "root")

# Настройки Redis
REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT: int = int(os.getenv("REDIS_PORT", 9000))
CACHE_EXPIRE_IN_SEC: int = 60

CELERY_BROKER_URL: str = "amqp://guest:guest@localhost:5672//"
CELERY_RESULT_BACKEND: str = "rpc://"

DATABASE_URL: str = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
# Корень проекта
BASE_DIR = os.path.join(BASEDIR, "files")
