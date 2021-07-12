from app.configs.database import db
from sqlalchemy import Column, Integer, String, VARCHAR
from werkzeug.security import check_password_hash, generate_password_hash


class Profile(db.Model):

    __tablename__ = 'Profiles'

    id = Column(Integer, primary_key=True)
    name = Column(String(127), nullable=False)
    last_name = Column(String(511), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(511), nullable=False)
    api_key = Column(VARCHAR(511), nullable=False)

    @property
    def password(self):
        raise AttributeError("Password is not acessible")

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def check_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)

    @property
    def serialized(self):
        return {"id":self.id, "name": self.name, "email": self.email}