FROM python:3

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

WORKDIR /greene_api

COPY . /greene_api/

RUN pip install -r requirements.txt

# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]