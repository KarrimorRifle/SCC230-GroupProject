import mysql.connector
from mysql.connector import Error
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
from threading import Lock, Thread
from queue import Queue

#db connection
# Create lock for cursor.execute
execute_lock = Lock()

# Create queue
execute_queue = Queue()

def execute_pending():
    while True:
        query = execute_queue.get()
        with execute_lock:
            cursor.execute(query)
        execute_queue.task_done()

# Start thread to execute pending queries
execute_thread = Thread(target=execute_pending)
execute_thread.daemon = True
execute_thread.start()

# Connection and cursor initialization
connection = mysql.connector.connect(
    user="user", password="pass", host="mysql", port=3306, database='DB'
)
print("DB connected")

cursor = connection.cursor(dictionary=True)

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

@app.errorhandler(mysql.connector.Error)
def reattemptConnection():
    while True:
        try:
            global connection
            connection = mysql.connector.connect(
                user = "user", password = "pass", host = "mysql", port=3306, database='DB'
            )
            print("DB connected")
            break
        except Exception as e:
            print(f"Error connecting to DB: {e}")

#Adds an error to the error log in the database
def addToErrorLog(exception:str):
    timestamp = datetime.strftime(datetime.now(UTC), "%Y-%m-%d %H-%M-%S")
    query = ("INSERT INTO error_log (Error, Time)"
             f"VALUES ('{exception}', '{timestamp}')")
    cursor.execute(query)


