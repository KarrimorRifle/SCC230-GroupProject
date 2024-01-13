import mysql.connector
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt

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
        if cursor.fetchone() is None:
            return
        else:
            return jsonify({"error": "Email already in use"}), 409
        

#running app
if __name__ == "__main__":
    app.run(debug = True, port=5050)
