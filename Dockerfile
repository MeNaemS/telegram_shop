FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV ENV_FOR_DYNACONF=production

ENV PYTHONPATH=/app

CMD ["python", "-m", "src.bootstrap.main"]