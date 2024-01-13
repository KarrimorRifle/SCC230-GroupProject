FROM alpine:3.19

RUN apk add --no-cache bash
RUN apk add --update py3-pip
RUN pip install mysql-connector-python flask flask-bcrypt --break-system-packages

WORKDIR /usr/app/src

COPY ./server.py ./
COPY ./wait-for-it.sh ./wait-for-it.sh

# Make the wait-for-it.sh script executable
RUN chmod +x ./wait-for-it.sh