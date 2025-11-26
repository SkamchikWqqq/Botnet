# database/users_db.py

# Временное хранилище пользователей и подписок
_users = set()
_subscriptions = {}

# --- Пользователи ---
def add_user(user_id):
    """Добавляет пользователя"""
    _users.add(user_id)

def remove_user(user_id):
    """Удаляет пользователя"""
    _users.discard(user_id)

def user_exists(user_id):
    """Проверяет, есть ли пользователь"""
    return user_id in _users

def all_users():
    """Возвращает список всех пользователей"""
    return list(_users)

# --- Подписки ---
def subscribe(user_id):
    """Подписка пользователя"""
    _subscriptions[user_id] = True

def unsubscribe(user_id):
    """Отписка пользователя"""
    _subscriptions[user_id] = False

def is_subscribed(user_id):
    """Проверяет, подписан ли пользователь"""
    return _subscriptions.get(user_id, False)
    
