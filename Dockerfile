# Используем базовый образ с Django
FROM python:3.12
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY req.txt /code/
RUN pip install -r req.txt
COPY . /code/