FROM python:3.13.6-alpine3.22

WORKDIR /app

COPY requirements.txt .

RUN apk add ffmpeg &&\
    pip install --upgrade pip &&\ 
    pip install -r requirements.txt &&\
    rm -rf requirements.txt 

COPY . .

CMD [ "python", "bot.py" ]