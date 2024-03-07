FROM python:3.8-slim

WORKDIR /app

# Installeer Git
RUN apt-get update
RUN apt-get install -y git

ENV GIT_SSL_NO_VERIFY=true

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY github_extract.py /app

CMD ["python", "github_extract.py"]