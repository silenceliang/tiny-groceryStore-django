FROM python:3.6.8
MAINTAINER silenceliang <"l3754902@gmail.com">
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["urMart/manage.py", "runserver"]

