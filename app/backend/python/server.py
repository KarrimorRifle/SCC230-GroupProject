import mysql.connector
from flask import Flask, request, jsonify, make_response
import bcrypt
import uuid
from datetime import datetime, timedelta

#db connection
connection = mysql.connector.connect(
    user = "root", password = "root", host = "host.docker.internal", port="3306", database='Accounts'
)
print("DB connected")

cursor = connection.cursor()

#setting up Flask
app = Flask(__name__)

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

@app.route("/accounts" , methods=['POST', 'PATCH', 'DELETE', 'GET'])
def accounts():
    #Creation of an account
    if request.method == 'POST':
        email = request.json.get('Email')
        query = ("SELECT * FROM accounts "
                 "WHERE Email = '{}'".format(email))
        cursor.execute(query)

        #creating a new account
        if cursor.fetchone() is None:
            sessionID = str(uuid.uuid4())
            sessionExpiry = datetime.now() + timedelta(days = 1)
            response = make_response(jsonify({"success":"Account created successfully"}))
            query = ("INSERT INTO accounts (FirstName, Surname, Email, `Password`, SessionID, SessionExp) "
                     "VALUES ('{}','{}','{}','{}','{}','{}')".format(request.json.get("FirstName"),request.json.get("Surname"),email,bcrypt.hashpw(request.json.get("Password").encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), sessionID, sessionExpiry))
            try:
                cursor.execute(query)
                connection.commit()
                response.set_cookie('session_id',sessionID, max_age=24*60*60)
                return response
            except Exception as e:
                connection.rollback()
                return jsonify({"error": str(e)}), 500
        #sending back error message
        else:
            return jsonify({"error" : "Email already in use"}), 409

    elif request.method == 'PATCH':
        account = getAccount()

        if account is None:
            return jsonify({"error": "Session ID is invalid"}), 401
        
        if (not request.json.get("password") is None) and bcrypt.checkpw(request.json.get('password').encode('utf-8'), account['Password'].encode('utf-8')):
            
            updateParams = []
            values = []
            for key, value in request.json.items():
                if not key[0].isupper():
                    continue
                updateParams.append(f"{key}=%s")
                values.append(value)
            updateParams = ', '.join(updateParams)

            query = ("UPDATE accounts "
                      f"SET {updateParams} "
                      "WHERE SessionID = %s AND AccountID = %s")
            values.extend([sessionID, account['AccountID']])

            try:
                cursor.execute(query, values)
                connection.commit()
                return jsonify({"success" : "Account has been successfully updated"})
            except Exception as e:
                connection.rollback()
                return jsonify({"error" : "Account couldn't be updated"}), 500
        
        else:
            return({"error": "Forbidden access"}), 401
        
    elif request.method == "DELETE":

        account = getAccount()

        if account is None:
            return jsonify({"error": "Session ID is invalid"}), 401
        
        if (not request.json.get("password") is None) and bcrypt.checkpw(request.json.get('password').encode('utf-8'), account['Password'].encode('utf-8')):
            query = (f"DELETE FROM accounts WHERE SessionID = {sessionID} AND AccountID = {account['AccountID']}" )
            try:
                cursor.execute(query)
                connection.commit()
                return(jsonify({"success":"Successfully deleted account!"}))
            except Exception as e:
                connection.rollback()
                return(jsonify({"error":"Unable to delete account"})), 500

        else:
            return({"error": "Forbidden access"}), 401
    
    elif request.method == "GET":
        account = getAccount()
        account.pop('Password', None)
        account.pop('SessionID', None)
        account.pop('SessionExp', None)
        if not (account is None):
            return jsonify(account)
        else:
            return 401
        

#running app
if __name__ == "__main__":
    app.run(debug = True, port=5000)
