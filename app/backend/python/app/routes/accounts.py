from flask import request, jsonify, make_response, Blueprint, current_app
import bcrypt
import uuid
from datetime import datetime, timedelta
from iota import genRandomID
from schedule.schedule import delete_schedule, get_schedules

accounts = Blueprint('accounts', __name__)


@accounts.route("/accounts" , methods=['POST', 'PATCH', 'DELETE', 'GET'])
def accountsResonse():
    cursor = current_app.config['cursor']
    connection= current_app.config['connection']
    #Creation of an account
    if request.method == 'POST':
        email = request.json.get('Email')
        query = ("SELECT * FROM accounts "
                 "WHERE Email = '{}'".format(email))
        cursor.execute(query)

        #creating a new account
        if cursor.fetchone() is None:
            query = ("SELECT AccountID FROM accounts")
            cursor.execute(query)
            accountIDs = cursor.fetchall()
            sessionID = str(uuid.uuid4())
            sessionExpiry = datetime.now() + timedelta(days = 1)
            response = make_response(jsonify({"success":"Account created successfully"}))
            query = ("INSERT INTO accounts (AccountID, FirstName, Surname, Email, `Password`, SessionID, SessionExp) "
                     "VALUES (%s,%s,%s,%s,%s,%s,%s)")
            try:
                cursor.execute(query, (genRandomID(ids=accountIDs,prefix="Acc"),request.json.get("FirstName"),request.json.get("Surname"),email,bcrypt.hashpw(request.json.get("Password").encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), sessionID, sessionExpiry,))
                connection.commit()
                response.set_cookie('session_id', sessionID, max_age=24*60*60)
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
        
        if (not request.json.get("Password") is None) and bcrypt.checkpw(request.json.get('Password').encode('utf-8'), account['Password'].encode('utf-8')):
            
            updateParams = []
            values = []
            for key, value in request.json.items():
                if not key[0].isupper():
                    continue
                if value == "":
                    continue
                updateParams.append(f"{key}=%s")
                if key == "Password":
                    value = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                values.append(value)
            updateParams = ', '.join(updateParams)

            query = ("UPDATE accounts "
                      f"SET {updateParams} "
                      "WHERE SessionID = %s AND AccountID = %s")
            values.extend([account['SessionID'], account['AccountID']])

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
        
        if (not request.json.get("Password") is None) and bcrypt.checkpw(request.json.get('Password').encode('utf-8'), account['Password'].encode('utf-8')):
            queries = [("DELETE FROM function_block_params WHERE AuthorID = %s" ),
                       ("DELETE FROM function_block_links WHERE AuthorID = %s" ),
                       ("DELETE FROM function_blocks WHERE AuthorID = %s" ),
                       ("DELETE FROM triggers WHERE AuthorID = %s" ),
                       ("DELETE FROM schedules WHERE AuthorID = %s" )]
            for query in queries:
                try:
                    cursor.execute(query, (account['AccountID'],))
                    connection.commit()
                except Exception as e:
                    connection.rollback()
                    return jsonify({"error": str(e)}), 500
            
            query = ("DELETE FROM accounts WHERE SessionID = %s AND AccountID = %s" )
            try:
                cursor.execute(query, (account['SessionID'], account['AccountID']))
                connection.commit()
                return(jsonify({"success":"Successfully deleted account!"}))
            except Exception as e:
                connection.rollback()
                return(jsonify({"error":"Unable to delete account", "details":f"{e}"})), 500

        else:
            return({"error": "Forbidden access"}), 401
    
    elif request.method == "GET":
        account = getAccount()
        if account == None:
            return jsonify({"error":"Session ID invalid"}), 403
        account.pop('Password', None)
        account.pop('SessionID', None)
        account.pop('SessionExp', None)
        if not (account is None):
            return jsonify(account)
        else:
            return 401
        
@accounts.route("/login", methods=["POST"])
def login():
    cursor = current_app.config['cursor']
    connection= current_app.config['connection']

    email = request.json.get("Email")
    password = request.json.get("Password")
    password = password.encode("utf-8")
    
    query = f"SELECT * FROM accounts WHERE Email = %s"
    try:
        cursor.fetchall()
    except:
        pass
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
    
@accounts.route("/logout", methods=["DELETE"])
def logout():
    cursor = current_app.config['cursor']
    connection= current_app.config['connection']

    sessionID = request.cookies.get('session_id')
    try:
        cursor.execute("UPDATE accounts SET SessionID = NULL, SessionExp = %s WHERE SessionID = %s",(datetime.now(), sessionID))
        connection.commit()
    except Exception as e:
        connection.rollback()
        return jsonify({'error':"Internal server error", "details":f"{e}"}), 500
    return 200
        
def getAccount():
    cursor = current_app.config['cursor']
    connection= current_app.config['connection']
    sessionID = request.cookies.get('session_id')
    query = ("SELECT * FROM accounts "
                "WHERE SessionID = %s")
    try:
        cursor.fetchall()
    except:
        pass
    finally:
        cursor.execute(query, (sessionID,))
        return cursor.fetchone()
