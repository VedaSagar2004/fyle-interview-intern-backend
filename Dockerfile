FROM python:3.8

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENV FLASK_APP=core/server.py

# RUN flask db upgrade -d core/migrations/

EXPOSE 5000

# CMD ["pytest", "-vvv", "-s", "tests/"]