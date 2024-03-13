FROM python:alpine3.19

ENV PYTHONUNBUFFERED 1

COPY /requirements.txt /tmp/requirements.txt
COPY ./app /python/app
WORKDIR /python/app

EXPOSE 5000

RUN python -m venv /py && \
    apk add --no-cache bash && \
    apk add py-pip && \
    pip install --upgrade pip && \
    apk add musl-dev gcc && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        pyuser


# Make the wait-for-it.sh script executable
RUN chmod +x ./wait-for-it.sh
CMD ["python", "./server.py"]

USER pyuser