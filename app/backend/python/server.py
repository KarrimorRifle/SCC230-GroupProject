import mysql.connector
from flask import Flask, request, jsonify, make_response
from flask_bcrypt import Bcrypt
import uuid
import datetime

#db connection
connection = mysql.connector.connect(
    user = "root", password = "root", host = "host.docker.internal", port="3306", database='Accounts'
)
print("DB connected")

cursor = connection.cursor()

#setting up Flask
app = Flask(__name__)
bcrypt = Bcrypt(app)

#handling paths and different methods
#@app.route("/path/<param>", methods = ['requestMethod1','requestMethod2'])
#def home(param):
#   if request.method == 'requestMethod1'
#    return "Home!"
#   else
#       return jsonify(object), statusCode
##getting query params
# var = request.args.get("queryParamName")

@app.route("/accounts" , methods=['POST', 'PATCH', 'DELETE'])
def accounts():
    #Creation of an account
    if request.method == 'POST':
        email = request.headers.get('email')
        query = ("SELECT * FROM accounts"
                 "WHERE Email = {}".format(email))
        cursor.execute(query)
        #creating a new account
        if cursor.fetchone() is None:
            query = ("INSERT INTO accounts VALUES (FirstName, Surname, Email, Pass)"
                     "({},{},{},{})".format(request.headers.get("firstName"),request.headers.get("surname"),email,request.headers.get("password")))
            try:
                cursor.execute(query)
                connection.commit()
                sessionID = str(uuid.uuid4())
                sessionExpiry = datetime.now() + datetime.timedelta(days = 1)
                response = make_response()
                response.set_cookie('session_id',sessionID, max_age=datetime.timedelta(days=1))
                return response
            except Exception as e:
                connection.rollback()
                return jsonify({"error": str(e)}), 500
        #sending back error message
        else:
            return jsonify({"error": "Email already in use"}), 409
        

#running app
if __name__ == "__main__":
    app.run(debug = True, port=5050)
