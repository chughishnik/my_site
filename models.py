from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Relationship
from databese import base

class User(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, index=True)
    password = Column(String, index=True)

class Quiz(base):
    __tablename__ = 'quizes'
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, index=True)
    question = Column(String)
    cor_answer = Column(String)
    answer1 = Column(String)
    answer2 = Column(String)
    answer3 = Column(String)
