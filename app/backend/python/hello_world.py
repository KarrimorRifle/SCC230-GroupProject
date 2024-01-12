import mysql.connector

connection = mysql.connector.connect(
    user = "root", password = "root", host = "mysql", port="3306", database='Accounts'
)

print("DB connected")

cursor = connection.cursor()
cursor.execute('Select * FROM accounts')
accounts = cursor.fetchall()
connection.close

print(accounts)