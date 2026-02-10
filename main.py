from fastapi import FastAPI, HTTPException, Path, Query, Body, Depends
from sqlalchemy.orm import Session
from typing import Optional, Annotated

from models import base, User, Quiz
from databese import engine, session_local
from schemas import user, quiz

app = FastAPI()

base.metadata.create_all(bind=engine)

def get_db():
    db=session_local()
    try:
        yield db
    finally:
        db.close()

@app.post('/register')
async def create_user(user: user, db: Session = Depends(get_db)):
    db_user = User(login=user.login, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@app.post('/create_quiz')
async def create_quiz(quiz:quiz, db: Session = Depends(get_db)):
    db_quiz = Quiz(label=quiz.label, cor_answer = quiz.cor_answer, answer1 = quiz.answer1, answer2 = quiz.answer2, answer3 = quiz.answer3, question = quiz.question)
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

@app.get('/')
async def home_page():
    return 'работает'

@app.get('/quiz/{id}')
async def quiz(id: int):
    pass
@app.get('/create')
async def create_quiz():
    pass