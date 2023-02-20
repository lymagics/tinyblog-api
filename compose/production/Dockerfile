FROM python:slim

COPY ./requirements /requirements
RUN pip install -r requirements/production.txt

WORKDIR /src
COPY ./src /src