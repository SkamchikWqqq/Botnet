# database/users_db.py

class UsersDB:
    """
    Минимальная база пользователей.
    Использует временное хранилище в памяти (set).
    """
    def __init__(self):
        self.users = set()

    def add_user(self, user_id):
        """Добавляет пользователя"""
        self.users.add(user_id)

    def remove_user(self, user_id):
        """Удаляет пользователя"""
        self.users.discard(user_id)

    def user_exists(self, user_id):
        """Проверяет, есть ли пользователь"""
        return user_id in self.users

    def all_users(self):
        """Возвращает список всех пользователей"""
        return list(self.users)


class SubscriptionDB:
    """
    Минимальная база подписок.
    Временное хранилище user_id -> True/False.
    """
    def __init__(self):
        self.subscriptions = {}

    def subscribe(self, user_id):
        """Подписка пользователя"""
        self.subscriptions[user_id] = True

    def unsubscribe(self, user_id):
        """Отписка пользователя"""
        self.subscriptions[user_id] = False

    def is_subscribed(self, user_id):
        """Проверяет, подписан ли пользователь"""
        return self.subscriptions.get(user_id, False)
      
