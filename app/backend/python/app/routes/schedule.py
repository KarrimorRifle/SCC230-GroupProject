from flask import request, jsonify, make_response, Blueprint, current_app
from .accounts import getAccount
from iota import genRandomID

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
    query = ("SELECT EventID FROM schedules")
    cursor.execute(query)
    scheduleIDs = cursor.fetchall()
    thisID = genRandomID(ids=scheduleIDs, prefix='Sch')
    query = ("INSERT INTO schedules (EventID, ScheduleName, AuthorID, IsActive, IsPublic, Rating) "
                     "VALUES (%s,%s,%s,%s,%s,%s)")
    try:
        cursor.execute(query, (thisID, scheduleName, account['AccountID'], request.json.get("IsActive"), request.json.get("IsPublic"), request.json.get('Rating'),))
        connection.commit()
    except Exception as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({'EventID':thisID}), 200

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

    code = []

    query = ("SELECT Link, ParentID FROM function_block_links "
             "WHERE ScheduleID = %s")
    cursor.execute(query, (scheduleID,))
    linkedCommands = cursor.fetchall()
    linkedCommands = [link for link in linkedCommands]

    query = ("SELECT Value, FunctionBlockID FROM function_block_params "
             "WHERE ScheduleID = %s")
    cursor.execute(query, (scheduleID,))
    params = cursor.fetchall()
    params = [param for param in params]

    links = []
    paramVals = []
    for block in functionBlocks:
        for link in linkedCommands:
            if link['ParentID'] == block['BlockID']:
                links.append(link['Link'])

        for param in params:
            if param['FunctionBlockID'] == block['BlockID']:
                paramVals.append(param['Value'])

        funcBlock = {'CommandType': block["CommandType"], 'Number': block["Num"], 'LinkedCommands': links, 'Params': paramVals}
        code.append(funcBlock)
        links = []
        paramVals = []

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

    for query in queries:
        cursor.execute(query, (scheduleID,))

    try:
        connection.commit()
    except:
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
    
    updateParams = []
    values = []
    newCode = [dict]
    newTriggers = []
    for key, value in request.json.items():
        if not key[0].isupper():
            continue
        if value == "":
            continue
        if key == "Code":
            newCode = value
            continue
        if key == "Triggers":
            newTriggers = value
            continue
        updateParams.append(f"{key}=%s")
        values.append(value)
    updateParams = ', '.join(updateParams)

    query = (f"UPDATE schedules SET {updateParams} WHERE EventID = %s AND AuthorID = %s")
    values.extend([scheduleID, account['AccountID']])

    try:
        cursor.execute(query, values)
        connection.commit()
    except Exception as e:
        connection.rollback()
        return jsonify({"error" : "Schedule couldn't be updated", "details":f"{e}"}), 500
    
    if newTriggers != []:
        query = ("DELETE FROM triggers WHERE ScheduleID = %s" )
        try:
            cursor.execute(query, (scheduleID,))
            connection.commit()
        except Exception as e:
            connection.rollback()
            return(jsonify({"error":"Unable to complete update schedule", "details":f"{e}"})), 500
        
        query = ("INSERT INTO triggers (TriggerName, ScheduleID, EventListenerID) "
                    "VALUES ")
        values = ()
        for trigger in newTriggers:
            query += ("(%s,%s,%s),")
            values += (trigger['TriggerName'], scheduleID, trigger['EventListenerID'],)

        query = query[:-1]
        try:
            cursor.execute(query, values)
            connection.commit()
        except Exception as e:
            connection.rollback()
            return(jsonify({"error":"Unable to update schedule triggers", "details":f"{e}"})), 500

    if newCode == []:
        return get_schedule_detail(account, cursor, scheduleID)

    queries = [("DELETE FROM function_blocks WHERE ScheduleID = %s" ),
               ("DELETE FROM function_block_params WHERE ScheduleID = %s" ),
               ("DELETE FROM function_block_links WHERE ScheduleID = %s" )]

    for query in queries:
        cursor.execute(query, (scheduleID,))

    try:
        connection.commit()
    except Exception as e:
        connection.rollback()
        return(jsonify({"error":"Unable to initiate update schedule code", "details":f"{e}"})), 500
    
    query = ("SELECT BlockID FROM function_blocks")
    cursor.execute(query)
    blockIDs = cursor.fetchall()

    queries = [("INSERT INTO function_blocks (BlockID, CommandType, Num, ScheduleID) "
                 "VALUES "),
                ("INSERT INTO function_block_links (ParentID, Link, ScheduleID) "
                 "VALUES "),
                ("INSERT INTO function_block_params (Value, FunctionBlockID, ScheduleID) "
                 "VALUES ")]
    values = [(), (), ()]

    for funcBlock in newCode:
        blockID = genRandomID(ids=blockIDs, prefix='Fun')

        queries[0] += ("(%s,%s,%s,%s),")
        values[0] += (blockID, funcBlock['CommandType'], funcBlock['Number'], scheduleID,)

        for link in funcBlock['LinkedCommands']:
            queries[1] += ("(%s,%s,%s),")
            values[1] += (blockID, link, scheduleID,)
            
        for param in funcBlock['Params']:
            queries[2] += ("(%s,%s,%s),")
            values[2] += (param, blockID, scheduleID,)

    i = 0
    for query in queries:
        query = query[:-1]
        cursor.execute(query, values[i])
        i+=1

    try:
        connection.commit()
    except Exception as e:
        connection.rollback()
        return(jsonify({"error":"Unable to update schedule code", "details":f"{e}"})), 500
            
    return get_schedule_detail(account, cursor, scheduleID)

@schedule.route("/schedule" , methods=['POST', 'GET'])
def scheduleResponse():
    #Get current user info
    account = getAccount()
    if account is None:
        return jsonify({"error": "Session ID is invalid"}), 401

    cursor = current_app.config['cursor']
    connection = current_app.config['connection']
    cursor.fetchall()

    if request.method == 'GET':
        return get_schedules(account, cursor)
    elif request.method == 'POST':
        return create_schedule(account, cursor, connection)

    cursor.close()
    connection.close()

# TO BE FIXED ONCE THE DATABASE CHANGES ARE MADE WITH IDs
@schedule.route("/schedule/<string:scheduleID>" , methods=['PATCH', 'DELETE', 'GET'])
def scheduleDetails(scheduleID):
    #Get current user info
    account = getAccount()
    if account is None:
        return jsonify({"error": "Session ID is invalid"}), 401

    cursor = current_app.config['cursor']
    connection = current_app.config['connection']
    cursor.fetchall()

    if request.method == 'GET':
        return get_schedule_detail(account, cursor, scheduleID)
    elif request.method == 'DELETE':
        return delete_schedule(account, cursor, connection, scheduleID)
    elif request.method == 'PATCH':
        return update_schedule(account, cursor, connection, scheduleID)

    cursor.close()
    connection.close()