import os


TOKEN = os.getenv("TOKEN")

admin_tg_id = 5312665858


def load_env_or_default(variable_name, default):
    if var := os.getenv(variable_name):
        pass
    else:
        var = default
    return var


""" WEBSOCKET """
WEBSOCKET_HOST = load_env_or_default('WEBSOCKET_HOST', 'localhost')
WEBSOCKET_CONNECTION_STRING = f'ws://{WEBSOCKET_HOST}:80/ws'

# УБРАТЬ ПОСЛЕ ПЕРЕНОСА В ФАСТАПИ!!!!!!
""" GRPC """
GRPC_HOST = load_env_or_default('GRPC_HOST', 'localhost')
GRPC_CONNECTION_STRING = f'{GRPC_HOST}:50051'

""" REDIS """
REDIS_HOST = load_env_or_default('REDIS_HOST', 'localhost')
REDIS_CONNECTION_STRING = f"redis://{REDIS_HOST}:6379/0"
