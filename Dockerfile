FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN mkdir -p /app/web/data

CMD ["python", "main.py"]
