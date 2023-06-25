from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from flask_login import UserMixin
from app import db, login_manager


@login_manager.user_loader
def get_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    # gender = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


class Candidate(db.Model):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    image = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    votes = Column(Integer, nullable=True, default=0)

    def __repr__(self):
        return f'<Candidate {self.first_name} {self.last_name}>'


class Vote(db.Model):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, nullable=False)
    president_id = Column(Integer, nullable=True)
    vice_president_id = Column(Integer, nullable=True)
    secretary_id = Column(Integer, nullable=True)

    # relationships
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
