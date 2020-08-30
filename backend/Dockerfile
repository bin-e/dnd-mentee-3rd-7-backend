FROM python:3

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

WORKDIR /greene_api

COPY . /greene_api/

RUN mkdir /greene_api/staticfiles

RUN pip install --upgrade pip

RUN pip install -r requirements.txt