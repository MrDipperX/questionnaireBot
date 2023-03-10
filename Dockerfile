FROM python:3.9-slim-buster
# set work directory
WORKDIR /questionnaireBot

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


CMD ["python", "main.py"]