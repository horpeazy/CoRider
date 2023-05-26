# dockerfile for corider image
#FROM python:latest

#WORKDIR /corider
#COPY . /corider

# install depedencies and setup db an static files

#RUN pip install -r --no-cache-dir requirements.txt
#RUN python manage.py collectstatic --noinput

#EXPOSE 8000

#ENTRYPOINT ["gunicorn", "corider.wsgi:application", "--bind", "0.0.0.0:8000"]


FROM python:latest AS package_cache

COPY cache /package_cache

FROM python:latest

COPY --from=package_cache /package_cache /package_cache

WORKDIR /corider

COPY . .

RUN pip install --no-index --find-links=/package_cache -r requirements.txt
RUN python manage.py collectstatic --noinput
