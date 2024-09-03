import os


def load_env_or_default(variable_name, default):
    if var := os.getenv(variable_name):
        pass
    else:
        var = default
    return var

# УБРАТЬ ПОСЛЕ ПЕРЕНОСА В ФАСТАПИ!!!!!!
""" GRPC """
GRPC_HOST = load_env_or_default('GRPC_HOST', 'localhost')
GRPC_CONNECTION_STRING = f'{GRPC_HOST}:50051'