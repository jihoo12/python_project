from dao.user_dao import UserDAO
from models.user import User

class UserService:
    def __init__(self, user_dao=None):
        self.user_dao = user_dao or UserDAO()

    def register(self, username, password, name, role="USER"):
        if not username or not password or not name:
            raise ValueError("All fields are required.")
        
        if self.user_dao.find_by_username(username):
            raise ValueError(f"Username '{username}' is already taken.")

        user = User(username=username, password=password, name=name, role=role)
        return self.user_dao.insert(user)

    def login(self, username, password):
        user = self.user_dao.find_by_username(username)
        if user and user.password == password:
            return user
        return None
