FROM python:3.13.1-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && pip install -r requirements.txt --timeout=1000

CMD uvicorn main:app --port=8000 --host=0.0.0.0
