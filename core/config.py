import sys
from os import environ, path

# Database configuration
DB_USER = environ.get("DB_USER", "db_user")
DB_PASSWORD = environ.get("DB_PASSWORD", "db_password")
DB_HOST = environ.get("DB_HOST", "localhost")
DB_PORT = environ.get("DB_PORT", "5432")
DB_NAME = environ.get("DB_NAME", "flight_assistant")
DB_SERVICE = environ.get("DB_SERVICE", "postgresql+asyncpg")

# HACK if pythest in loaded modules, enable testing mode
TESTING = environ.get("TESTING", "false").lower() == "true" or "pytest" in sys.modules

if TESTING:
    DB_NAME = f"{DB_NAME}_test"

DATABASE_URL = f"{DB_SERVICE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

AUTH_TOKEN = environ.get("AUTH_TOKEN", "X-Token")

# ImgKit settings
WKHTMLTOIMAGE_PATH = environ.get("WKHTMLTOIMAGE_PATH", "/usr/bin/wkhtmltoimage")

# REDIS settings
REDIS_HOST = environ.get("REDIS_HOST", "localhost")
REDIS_PORT = environ.get("REDIS_PORT", "6379")
REDIS_DB = environ.get("REDIS_DB", "13")

# Others
DEBUG_PORT = int(environ.get("DEBUG_PORT", 8002))
ROOT_DIR = path.dirname(path.dirname(__file__))

# Alembic
ALEMBIC_ENV_FILE_DIR = path.join(ROOT_DIR, "alembic")
ALEMBIC_INI_FILE_PATH = path.join(ROOT_DIR, "alembic.ini")
ALEMBIC_UNIT_TEST_MIGRATIONS_DIR = path.join(ROOT_DIR, "alembic/unittest")
