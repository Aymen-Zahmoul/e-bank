# Database schemas / models (e.g., SQLAlchemy standard or raw dict models)

class User:
    def __init__(self, id: int, email: str, name: str):
        self.id = id
        self.email = email
        self.name = name
