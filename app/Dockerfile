FROM ubuntu:16.04
RUN apt-get update -y --fix-missing
RUN apt-get install -y python-pip python-dev build-essential sqlite3
COPY ./ /app
WORKDIR /app
RUN pip install Flask flask_sqlalchemy sqlalchemy
ENTRYPOINT ["python"]
CMD ["data.py"]
