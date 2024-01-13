import mysql.connector
from flask import Flask, request, jsonify

#db connection
connection = mysql.connector.connect(
    user = "root", password = "root", host = "host.docker.internal", port="3306", database='Accounts'
)
print("DB connected")

#setting up a port to listen on
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


if __name__ == "__main__":
    app.run(debug = True, port=5050)
