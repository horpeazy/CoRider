# dockerfile for corider image
FROM python:slim

WORKDIR /corider
COPY . .

RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput

EXPOSE 8000

