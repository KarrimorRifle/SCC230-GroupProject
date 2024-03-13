import mysql.connector
from flask import Flask
from flask_cors import CORS
from routes.accounts import accounts
from routes.schedule.schedule import schedule
from routes.hub.hub import hub
from routes.hub.device.device import device
from routes.hub.schedule.hub_schedule import hub_schedule
from routes.hub.user.hub_user import hub_user
from routes.schedule.public_schedule.public_schedule import public_schedule
from datetime import datetime, UTC

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
app.register_blueprint(device)
app.register_blueprint(hub_schedule)
app.register_blueprint(hub_user)
app.register_blueprint(public_schedule)
CORS(app, supports_credentials=True)

#Adds an error to the error log in the database
def addToErrorLog(exception:str):
    cursor = app.config['cursor']
    timestamp = datetime.strftime(datetime.now(UTC), "%Y-%m-%d %H-%M-%S")
    query = ("INSERT INTO error_log (Error, Time)"
             f"VALUES ('{exception}', '{timestamp}')")
    cursor.execute(query)

#running app
if __name__ == "__main__":
    app.run(debug = True, port=5000)
