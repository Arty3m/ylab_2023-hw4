import os
from pathlib import Path

VERSION: str = "1.0.0"

# Название проекта. Используется в Swagger-документации
PROJECT_NAME: str = os.getenv("PROJECT_NAME", "ylab_2023_hw2")

# Настройки Postgres
POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_DB: str = os.getenv("POSTGRES_DB", "ylab_hw")
POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "root")

DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Корень проекта
BASE_DIR = Path(__file__).resolve().parent.parent
