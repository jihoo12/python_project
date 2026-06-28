class User:
    def __init__(self, username, password, name, role="USER", id=None):
        self.id = id
        self.username = username
        self.password = password
        self.name = name
        self.role = role

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "name": self.name,
            "role": self.role
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            username=data.get("username"),
            password=data.get("password"),
            name=data.get("name"),
            role=data.get("role", "USER")
        )
