FROM python:3

COPY . /code/
RUN pip install -r /code/requirements.txt