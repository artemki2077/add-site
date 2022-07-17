FROM python:3.7-stretch
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev gunicorn build-essential 
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["gunicorn -b :$PORT app:app"]