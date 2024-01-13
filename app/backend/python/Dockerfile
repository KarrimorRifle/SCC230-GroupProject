FROM alpine:3.19

RUN apk add --update py3-pip
RUN set -e; \
        apk add --no-cache --virtual .build-deps \
                gcc \
                libc-dev \
                linux-headers \
                mariadb-dev \
                python3-dev \
                postgresql-dev \
        ;
RUN pip install mysql-connector-python flask flask-bycrypt--break-system-packages

WORKDIR /usr/app/src

COPY ./server.py ./