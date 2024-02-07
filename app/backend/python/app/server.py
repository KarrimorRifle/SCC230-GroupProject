import mysql.connector
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from iota.User import user

#db connection
connection = mysql.connector.connect(
    user = "user", password = "pass", host = "mysql", port="3306", database='DB'
)
print("DB connected")

cursor = connection.cursor(dictionary = True)

#setting up Flask
app = Flask(__name__)
app.config['cursor'] = cursor
app.config['connection'] = connection
app.register_blueprint(user)
CORS(app, supports_credentials=True)

#running app
if __name__ == "__main__":
    app.run(debug = True, port=5000)
