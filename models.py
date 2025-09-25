from dataclasses import dataclass
from typing import List

@dataclass
class Choice:
    text: str
    
@dataclass
class Question:
    text: str
    choices: List[Choice]
    correct_index: int
    
@dataclass
class QuizDraft:
    title: str
    questions: List[Question]
    