import os


def load_env_or_default(variable_name, default):
    if var := os.getenv(variable_name):
        pass
    else:
        var = default
    return var


""" DATABASE """
POSTGRES_HOST = load_env_or_default('POSTGRES_HOST', 'localhost')
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = load_env_or_default('POSTGRES_USER', 'local')
POSTGRES_PASSWORD = load_env_or_default('POSTGRES_PASSWORD', 'local')
print(POSTGRES_DB)
DATABASE_URL_SYNC = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'
print(DATABASE_URL_SYNC)

""" REDIS """
REDIS_HOST = load_env_or_default('REDIS_HOST', 'localhost')
REDIS_CONNECTION_STRING = f"redis://{REDIS_HOST}:6379/0"

""" GRPC """
GRPC_HOST = load_env_or_default('GRPC_HOST', 'localhost')
GRPC_CONNECTION_STRING = f'{GRPC_HOST}:50051'
