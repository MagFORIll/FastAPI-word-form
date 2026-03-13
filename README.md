## Установка
pip install -r requirements.txt
### Запуск сайта (можно запустить через app.py)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

docker run -d -p 6379:6379 --name redis redis:alpine

### API Документация
http://localhost:8000/docs 