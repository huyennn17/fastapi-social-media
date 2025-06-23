from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable = False, autoincrement=True)
    title = Column(String(255), nullable = False)
    content = Column(String(255), nullable = False)
    published = Column(Boolean, server_default= "True", nullable = False)
    created_at = Column(TIMESTAMP (timezone=True), nullable = False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), nullable = False)
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable = False, autoincrement=True)
    email = Column(String(255), nullable = False, unique=True)
    password = Column(String(255), nullable = False)
    created_at = Column(TIMESTAMP (timezone=True), nullable = False, server_default=text('now()'))

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)

    user = relationship("User")
    post = relationship("Post")