
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql import quoted_name
from app.db.base import Base
from werkzeug.security import generate_password_hash, check_password_hash

class User(Base):
    __tablename__ = quoted_name("user", True)

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(200), nullable=False)

    def set_password(self, raw: str):
        self.password = generate_password_hash(raw)

    def check_password(self, raw: str) -> bool:
        return check_password_hash(self.password, raw)
