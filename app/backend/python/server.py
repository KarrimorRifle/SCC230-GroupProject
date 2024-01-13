import mysql.connector
from flask import Flask, request, jsonify, make_response
import bcrypt
import uuid
from datetime import datetime, timedelta
from routes.accounts import accounts

#db connection
connection = mysql.connector.connect(
    user = "root", password = "root", host = "host.docker.internal", port="3306", database='Accounts'
)
print("DB connected")

cursor = connection.cursor()

#setting up Flask
app = Flask(__name__)
app.register_blueprint(accounts)

#handling paths and different methods
#@app.route("/path/<param>", methods = ['requestMethod1','requestMethod2'])
#def home(param):
#   if request.method == 'requestMethod1'
#    return "Home!"
#   else
#       return jsonify(object), statusCode
##getting query params
# var = request.args.get("queryParamName")

def getAccount():
    sessionID = request.cookies.get('session_id')
    query = ("SELECT * FROM accounts "
                "WHERE SessionID = '{}'".format(sessionID))
    
    cursor.execute(query)
    return cursor.fetchone()

        

#running app
if __name__ == "__main__":
    app.run(debug = True, port=5000)
