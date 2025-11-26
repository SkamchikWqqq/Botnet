# database/users_db.py

# Временное хранилище пользователей и подписок
_users = set()
_subscriptions = {}

# --- Пользователи ---
def add_user(user_id):
    _users.add(user_id)

def remove_user(user_id):
    _users.discard(user_id)

def user_exists(user_id):
    return user_id in _users

def all_users():
    return list(_users)

def count_users():
    """Возвращает количество пользователей"""
    return len(_users)

# --- Подписки ---
def subscribe(user_id):
    _subscriptions[user_id] = True

def unsubscribe(user_id):
    _subscriptions[user_id] = False

def is_subscribed(user_id):
    return _subscriptions.get(user_id, False)
