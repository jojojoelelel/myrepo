FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y ffmpeg

EXPOSE 8001

CMD ['python', 'asr_api.py']