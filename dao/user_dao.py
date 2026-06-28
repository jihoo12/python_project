from dao.base_dao import BaseDAO
from models.user import User

class UserDAO(BaseDAO):
    def __init__(self, file_path="data/users.json"):
        super().__init__(file_path)

    def find_all(self):
        data = self._read_all()
        return [User.from_dict(item) for item in data]

    def find_by_username(self, username):
        users = self.find_all()
        for user in users:
            if user.username == username:
                return user
        return None

    def insert(self, user):
        users = self.find_all()
        if self.find_by_username(user.username):
            raise ValueError(f"Username '{user.username}' already exists.")
        
        max_id = max([u.id for u in users if u.id is not None], default=0)
        user.id = max_id + 1
        
        users.append(user)
        self._write_all([u.to_dict() for u in users])
        return user

    def update(self, user):
        users = self.find_all()
        for idx, u in enumerate(users):
            if u.id == user.id:
                users[idx] = user
                self._write_all([x.to_dict() for x in users])
                return True
        return False
