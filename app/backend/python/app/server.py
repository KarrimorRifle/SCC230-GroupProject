import mysql.connector
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import bcrypt
import uuid
from datetime import datetime, timedelta
from routes.accounts import accounts
from routes.hub import hub

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
app.register_blueprint(accounts)
app.register_blueprint(hub)
CORS(app, supports_credentials=True)

#handling paths and different methods
#@app.route("/path/<param>", methods = ['requestMethod1','requestMethod2'])
#def home(param):
#   if request.method == 'requestMethod1'
#    return "Home!"
#   else
#       return jsonify(object), statusCode
##getting query params
# var = request.args.get("queryParamName")
@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("Email")
    password = request.json.get("Password")
    password = password.encode("utf-8")
    
    query = f"SELECT * FROM accounts WHERE Email = %s"
    cursor.execute(query, (email,))
    account = cursor.fetchone()
    if account is None:
        return jsonify({"error":"Details don't match our system"}), 403

    if bcrypt.checkpw(password, account.get("Password").encode("utf-8")):
        response = make_response(jsonify({"success":"Logged in successfully"}))
        sessionID = str(uuid.uuid4())
        sessionExp = datetime.now() + timedelta(days = 1)

        try:
            cursor.execute("UPDATE accounts SET SessionID = %s, SessionExp = %s WHERE AccountID = %s",(sessionID,sessionExp,account.get("AccountID")))
            connection.commit()
        except Exception as e:
            connection.rollback()
            return jsonify({'error':"Internal server error", "details":f"{e}"}), 500
        
        response.set_cookie('session_id', sessionID, max_age=24*60*60)
        return(response)

    else:
        return jsonify({"error":"Details don't match our system"}), 403

def getAccount():
    sessionID = request.cookies.get('session_id')
    query = ("SELECT * FROM accounts "
                "WHERE SessionID = %s")
    
    cursor.execute(query, (sessionID))
    return cursor.fetchone()
        

#running app
if __name__ == "__main__":
    app.run(debug = True, port=5000)
