FROM python:slim

COPY ./requirements /requirements
RUN pip install -r requirements/development.txt

WORKDIR /src
COPY ./src /src