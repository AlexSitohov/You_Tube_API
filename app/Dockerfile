FROM python:alpine

WORKDIR /app

COPY . .

ENV SMTP_USER="lilinfinitemob@gmail.com"
    SMTP_PASSWORD="zhfpjgqopauywzvm"


RUN pip install -r req.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]