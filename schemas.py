from pydantic import BaseModel

class user(BaseModel):
    login: str
    password: str
    id: int

class quiz(BaseModel):
    label: str
    question: str
    cor_answer: str
    answer1: str
    answer2: str
    answer3: str
    id: int

