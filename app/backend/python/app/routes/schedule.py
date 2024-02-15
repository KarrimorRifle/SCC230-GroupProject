from flask import request, jsonify, make_response, Blueprint, current_app
from .accounts import getAccount

schedule = Blueprint('schedule', __name__)

# Function returns list of schedules linked to user who is logged in
def get_schedules(account, cursor):
    query = ("SELECT EventID, ScheduleName, IsActive, IsPublic, Rating FROM schedules "
                "WHERE AuthorID = %s")
    
    cursor.execute(query, (account['AccountID'],))
    schedules = cursor.fetchall()
    return jsonify(schedules), 200

#TO BE UPDATED BASED ON DATABASE ID CHANGES
def create_schedule(account, cursor, connection):
    # ADD SCHEDULE ID CHANGES TO ENTER INTO DB BASED ON FUTURE CHANGES
    scheduleName = request.json.get("ScheduleName")
    query = ("INSERT INTO schedules (ScheduleName, AuthorID, IsActive, IsPublic, Rating) "
                     "VALUES ('{}','{}','{}','{}','{}')".format(scheduleName, account['AccountID'], request.json.get("IsActive"), request.json.get("IsPublic"), request.json.get('Rating')))
    try:
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 500
    
    # UPDATE THIS SECTION BASED ON ID CHANGES IN DB
    query = ("SELECT EventID FROM schedules "
                "WHERE ScheduleName = %s AND AuthorID = %s")
    
    cursor.execute(query, (scheduleName, account['AccountID'],))

    scheduleID = cursor.fetchone()

    if scheduleID is None:
        return jsonify({"error":"Schedule ID could not be retrieved"}), 500

    return jsonify(scheduleID), 200

def get_schedule_detail(account, cursor, scheduleID):
    query = ("SELECT * FROM schedules "
                "WHERE AuthorID = %s AND EventID = %s")
    cursor.execute(query, (account['AccountID'], scheduleID,))
    schedule = cursor.fetchone()

    if schedule is None:
        return 401

    query = ("SELECT * FROM function_blocks "
                "WHERE ScheduleID = %s")
    cursor.execute(query, (scheduleID,))
    functionBlocks = cursor.fetchall()

    # FIX TRIGGER IN DATABASE TO MATCH TRIGGER CLASS THEN SORT THIS
    query = ("SELECT TriggerID, TriggerName, EventListenerID FROM triggers "
                "WHERE ScheduleID = %s")
    cursor.execute(query, (scheduleID,))
    triggers = cursor.fetchall()

    emptyBlock = {'CommandType': '', 'Number': 0, 'LinkedCommands': [int], 'Params': [str]}
    code = [emptyBlock for _ in range(len(functionBlocks))]

    i = 0
    for block in functionBlocks:
        query = ("SELECT Link FROM function_block_links "
                "WHERE ScheduleID = %s AND ParentID = %s")
        cursor.execute(query, (scheduleID, block['BlockID'],))
        linkedCommands = cursor.fetchall()

        query = ("SELECT Value FROM function_block_params "
                "WHERE ScheduleID = %s AND ParentID = %s")
        cursor.execute(query, (scheduleID, block['BlockID'],))
        params = cursor.fetchall()

        funcBlock = {'CommandType': block["CommandType"], 'Number': block["Num"], 'LinkedCommands': linkedCommands, 'Params': params}
        code[i] = funcBlock
        i+=1

    details = {'EventID': schedule['EventID'],
               'AuthorID': schedule['AuthorID'],
               'ScheduleName': schedule['ScheduleName'],
               'IsActive': schedule['IsActive'],
               'IsPublic': schedule['IsPublic'],
               'Rating': schedule['Rating'],
               'Code': code,
               'Triggers': triggers}
    
    return jsonify(details), 200

# Function deletes schedule of specified ID as long as user is the author
def delete_schedule(account, cursor, connection, scheduleID):
    query = ("SELECT EventID FROM schedules "
                "WHERE AuthorID = %s AND EventID = %s")
    cursor.execute(query, (account['AccountID'], scheduleID,))
    checkID = cursor.fetchone()

    if checkID is None:
        return({"error": "Forbidden access"}), 401

    queries = [("DELETE FROM schedules WHERE EventID = %s" ),
               ("DELETE FROM function_blocks WHERE ScheduleID = %s" ),
               ("DELETE FROM function_block_params WHERE ScheduleID = %s" ),
               ("DELETE FROM function_block_links WHERE ScheduleID = %s" ),
               ("DELETE FROM triggers WHERE ScheduleID = %s" )]

    for i in range(len(queries)):
        try:
            cursor.execute(queries[i], (scheduleID,))
            connection.commit()
        except Exception as e:
            connection.rollback()
            return(jsonify({"error":"Unable to delete schedule", "details":f"{e}"})), 500

    return jsonify(scheduleID), 200

# WORK IN PROGRESS
def update_schedule(account, cursor, connection, scheduleID):
    query = ("SELECT EventID FROM schedules "
                "WHERE AuthorID = %s AND EventID = %s")
    cursor.execute(query, (account['AccountID'], scheduleID,))
    checkID = cursor.fetchone()

    if checkID is None:
        return({"error": "Forbidden access"}), 401

@schedule.route("/schedule" , methods=['POST', 'GET'])
def scheduleResponse():
    #Get current user info
    account = getAccount()
    if account is None:
        return jsonify({"error": "Session ID is invalid"}), 401

    cursor = current_app.config['cursor']
    connection = current_app.config['connection']

    if request.method == 'GET':
        return get_schedules(account, cursor)
    elif request.method == 'POST':
        return create_schedule(account, cursor, connection)

    cursor.close()
    connection.close()

# TO BE FIXED ONCE THE DATABASE CHANGES ARE MADE WITH IDs
@schedule.route("/schedule/<int:scheduleID>" , methods=['PATCH', 'DELETE', 'GET'])
def scheduleDetails(scheduleID):
    #Get current user info
    account = getAccount()
    if account is None:
        return jsonify({"error": "Session ID is invalid"}), 401

    cursor = current_app.config['cursor']
    connection = current_app.config['connection']

    if request.method == 'GET':
        return get_schedule_detail(account, cursor, scheduleID)
    elif request.method == 'DELETE':
        return delete_schedule(account, cursor, connection, scheduleID)
    elif request.method == 'PATCH':
        return update_schedule(account, cursor, connection, scheduleID)

    cursor.close()
    connection.close()