from app.configs.database import db
from sqlalchemy import Column, Integer, String, VARCHAR

class Profile(db.Model):

    __tablename__ = 'Profiles'

    id = Column(Integer, primary_key=True)
    name = Column(String(127), nullable=False)
    last_name = Column(String(511), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(511), nullable=False)
    api_key = Column(VARCHAR(511), nullable=False)

    @property
    def serialized(self):
        return {"id":self.id, "name": self.name, "email": self.email}