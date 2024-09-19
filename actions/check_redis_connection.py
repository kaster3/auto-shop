from api.api_v1.cache import get_redis_connection


def set_user_count():
    redis_connection = get_redis_connection()
    if redis_connection.ping():  # Проверка соединения
        redis_connection.set("user_count", 1)
        redis_connection.set("users_count", 3)
        print("User count set successfully.")
    else:
        print("Failed to connect to Redis.")
