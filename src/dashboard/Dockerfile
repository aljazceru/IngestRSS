FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install fastapi uvicorn pymongo

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
