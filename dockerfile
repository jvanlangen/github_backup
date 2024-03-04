FROM python:3.8-slim

WORKDIR /app

# Installeer Git
RUN apt-get update && apt-get install -y git

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py /app

CMD ["python", "main.py"]