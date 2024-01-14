FROM python

# RUN apk add --no-cache bash
# RUN apk add --update py3-pip
# RUN apk add --update musl-dev gcc cargo
RUN pip install mysql-connector-python flask bcrypt flask-cors

WORKDIR /usr/app/src

COPY ./server.py ./
COPY ./wait-for-it.sh ./wait-for-it.sh

# Make the wait-for-it.sh script executable
RUN chmod +x ./wait-for-it.sh
EXPOSE 5000
CMD ["python", "./server.py"]