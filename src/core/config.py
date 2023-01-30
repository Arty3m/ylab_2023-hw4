import os
from pathlib import Path

VERSION: str = '1.0.0'

# Название проекта. Используется в Swagger-документации
PROJECT_NAME: str = os.getenv('PROJECT_NAME', 'ylab_2023_hw3')

# Настройки Postgres
POSTGRES_HOST: str = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT: int = int(os.getenv('POSTGRES_PORT', 5432))
POSTGRES_DB: str = os.getenv('POSTGRES_DB', 'ylab_hw')
POSTGRES_USER: str = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', 'root')

# Настройки Redis
REDIS_HOST: str = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT: int = int(os.getenv('REDIS_PORT', 9000))
CACHE_EXPIRE_IN_SEC: int = 60 * 5

DATABASE_URL: str = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
print('from config', DATABASE_URL)
# Корень проекта
BASE_DIR = Path(__file__).resolve().parent.parent
