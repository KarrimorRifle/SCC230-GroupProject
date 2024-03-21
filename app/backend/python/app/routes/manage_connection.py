import mysql.connector

def reattemptConnection():
    while True:
        try:
            connection = mysql.connector.connect(
                user = "user", password = "pass", host = "mysql", port=3306, database='DB'
            )
            print("DB connected")
            break
        except Exception as e:
            print(f"Error connecting to DB: {e}")

    return connection