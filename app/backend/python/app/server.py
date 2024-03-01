import mysql.connector
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from routes.accounts import accounts
from routes.schedule.schedule import schedule
from routes.hub.hub import hub
from routes.hub.user.hub_user import hub_user

#db connection
connection = mysql.connector.connect(
    user = "user", password = "pass", host = "mysql", port=3306, database='DB'
)
print("DB connected")

cursor = connection.cursor(dictionary = True)

#setting up Flask
app = Flask(__name__)
app.config['cursor'] = cursor
app.config['connection'] = connection
app.register_blueprint(accounts)
app.register_blueprint(schedule)
app.register_blueprint(hub)
app.register_blueprint(hub_user)
CORS(app, supports_credentials=True)

#running app
if __name__ == "__main__":
    app.run(debug = True, port=5000)
