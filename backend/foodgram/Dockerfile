FROM python:3.7-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    build-essential

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip && pip3 install -r requirements.txt --no-cache-dir

COPY ./ .

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]