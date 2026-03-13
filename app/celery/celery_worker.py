from celery import Celery
from app.services.services import find_word_form
import json

app = Celery('word_analyzer', broker='redis://localhost:6379/0')

@app.task
def process_file_task(content: str, json_path: str):
    """Celery задача"""
    result = find_word_form(content)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False)
    return json_path
