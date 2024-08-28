import os


def load_env_or_default(variable_name, default):
    if var := os.getenv(variable_name):
        pass
    else:
        var = default
    return var


""" DATABASE """
POSTGRES_USER = load_env_or_default('POSTGRES_USER', 'local')
POSTGRES_PASSWORD = load_env_or_default('POSTGRES_PASSWORD', 'local')
POSTGRES_HOST = load_env_or_default('POSTGRES_HOST', 'localhost')
POSTGRES_DB = load_env_or_default('POSTGRES_DB', 'local')
DATABASE_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'

