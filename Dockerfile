# dockerfile for corider image
FROM python:latest

WORKDIR /corider
COPY . /corider

# install depedencies and setup db an static files

RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput

EXPOSE 8000

#ENTRYPOINT ["gunicorn", "corider.wsgi:application", "--bind", "0.0.0.0:8000"]

