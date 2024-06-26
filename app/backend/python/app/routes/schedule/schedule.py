from flask import request, jsonify, Blueprint, current_app
from ..accounts import getAccount
from iota import genRandomID

schedule = Blueprint('schedule', __name__)

# Function returns list of schedules linked to user who is logged in
def get_schedules(account, cursor):
    query = ("SELECT ScheduleID, ScheduleName, IsActive, IsPublic, Rating, IsDraft, CopyFrom FROM schedules "
                "WHERE AuthorID = %s "
                "ORDER BY IsActive DESC, ScheduleName")
    
    cursor.execute(query, (account['AccountID'],))
    schedules = cursor.fetchall()

    return jsonify(schedules), 200

#TO BE UPDATED BASED ON DATABASE ID CHANGES
def create_schedule(account, cursor, connection, schedule):
    scheduleName = schedule.get('ScheduleName')
    scheduleAuthor = schedule.get('AuthorID')
    if scheduleAuthor is None:
        scheduleAuthor = account['AccountID']

    if scheduleName is None:
        return jsonify({"error": "ScheduleName is required"}), 400

    query = ("SELECT ScheduleID FROM schedules")
    cursor.execute(query)
    scheduleIDs = cursor.fetchall()
    thisID = genRandomID(ids=scheduleIDs, prefix='Sch')
    query = ("INSERT INTO schedules (ScheduleID, ScheduleName, AuthorID) "
                     "VALUES (%s,%s,%s)")
    try:
        cursor.execute(query, (thisID, scheduleName, scheduleAuthor))
        connection.commit()
    except Exception as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({'ScheduleID':thisID}), 200

def get_schedule_detail(account, cursor, scheduleID, hubCall=False):
    query = ("SELECT ScheduleID FROM schedules "
                "WHERE AuthorID = %s AND ScheduleID = %s")
    cursor.execute(query, (account['AccountID'], scheduleID,))
    checkID = cursor.fetchone()

    query = ("SELECT * FROM schedules "
                "WHERE ScheduleID = %s")
    cursor.execute(query, (scheduleID,))
    schedule = cursor.fetchone()

    if schedule is None:
        return jsonify({"error": "Schedule not found"}), 404

    if checkID is None and hubCall is False:
        return 401

    query = ("SELECT * FROM function_blocks "
                "WHERE ScheduleID = %s")
    cursor.execute(query, (scheduleID,))
    functionBlocks = cursor.fetchall()

    query = ("SELECT TriggerID FROM triggers "
                "WHERE ScheduleID = %s")
    cursor.execute(query, (scheduleID,))
    trigger = cursor.fetchone()

    triggerArr = []
    if trigger is not None:
        query = ("SELECT Data FROM trigger_data "
                    "WHERE TriggerID = %s")
        cursor.execute(query, (trigger['TriggerID'],))
        triggerData = cursor.fetchall()

        for data in triggerData:
            triggerArr.append(data['Data'])

    code = []
    varDict = {}

    query = ("SELECT Link, ParentID FROM function_block_links "
             "WHERE ScheduleID = %s")
    cursor.execute(query, (scheduleID,))
    linkedCommands = cursor.fetchall()
    linkedCommands = [link for link in linkedCommands]

    query = ("SELECT Value, FunctionBlockID, ListPos FROM function_block_params "
             "WHERE ScheduleID = %s ORDER BY ListPos")
    cursor.execute(query, (scheduleID,))
    params = cursor.fetchall()

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
    for i in range(2):
        for j in range(len(code)):
            for x in range(len(code[j]['Params'])):
                sVariable = code[j]['Params'][x].split('.')
                if(sVariable[0] == 'var'):
                    svalue = [""]
                    if(code[j]['CommandType'] == "SET"):
                        if(x==0):
                            svalue = code[j]['Params'][2].split('.')
                        else:
                            svalue = code[j]['Params'][0].split('.')
                    VarDictUpdate(sVariable[1], svalue, varDict)

    code = sorted(code, key=lambda x: x['Number'])

    details = {'ScheduleID': schedule['ScheduleID'],
               'AuthorID': schedule['AuthorID'],
               'CopyFrom': schedule['CopyFrom'],
               'ScheduleName': schedule['ScheduleName'],
               'Description': schedule['Description'],
               'HubID': schedule['HubID'],
               'IsActive': schedule['IsActive'],
               'IsPublic': schedule['IsPublic'],
               'IsDraft': schedule['IsDraft'],
               'Rating': schedule['Rating'],
               'Code': code,
               'VarDict': varDict,
               'Trigger': triggerArr}
    
    return jsonify(details), 200

def VarDictUpdate(variable, svalue, varDict):
    try:
        if(variable in varDict):
            if(svalue[0] == 'var' and svalue[1] in varDict):
                if(varDict[svalue[1]] !=  varDict[variable]):
                    if (varDict[variable] == "UNDEFINED"):
                        varDict.update({variable:varDict[svalue[1]]})
                    else:
                        varDict.update({variable,"INCONSISTENT"})
            else:
                if(svalue[0] == "" or svalue[1] not in varDict):
                    varDict.update({variable:"UNDEFINED"})
                else:
                    exec(f"{'var = ' + svalue[0]}")
                    if(type(var) == str and varDict[variable] != "STRING"):
                        varDict.update({variable:"INCONSISTENT"})
                    if(type(var) == bool and varDict[variable] != "BOOLEAN"):
                        varDict.update({variable:"INCONSISTENT"})
                    else:
                        if(type(var) == bool or type(var) == str):
                            varDict.update({variable:"INCONSISTENT"})
        else:
            if(svalue[0] == 'var' and svalue[1] in varDict):
                varDict.update({variable:varDict[svalue[1]]})
            else:
                if(svalue[0] == "" or svalue[1] not in varDict):
                    varDict.update({variable:"UNDEFINED"})
                else:
                    value = svalue[0]
                    exec(f"{'var = ' + value}")
                    if(type(var) == str):
                        varDict.update({variable:"STRING"})
                    if(type(var) == bool):
                        varDict.update({variable:"BOOLEAN"})
                    else:
                        varDict.update({variable:"NUMBER"})
    except Exception as e:
        #error handler here
        pass

# Function deletes schedule of specified ID as long as user is the author
def delete_schedule(account, cursor, connection, scheduleID, hubCall=False):
    query = ("SELECT ScheduleID FROM schedules "
                "WHERE AuthorID = %s AND ScheduleID = %s")
    cursor.execute(query, (account['AccountID'], scheduleID,))
    checkID = cursor.fetchone()

    if checkID is None and hubCall is False:
        return({"error": "Forbidden access"}), 401
    
    query = ("SELECT TriggerID FROM triggers "
                "WHERE ScheduleID = %s")
    cursor.execute(query, (scheduleID,))
    trigger = cursor.fetchone()

    if trigger is not None:
        query = ("DELETE FROM trigger_data WHERE TriggerID = %s")
        cursor.execute(query, (trigger['TriggerID'],))

    queries = [("DELETE FROM function_block_params WHERE ScheduleID = %s" ),
               ("DELETE FROM function_block_links WHERE ScheduleID = %s" ),
               ("DELETE FROM function_blocks WHERE ScheduleID = %s" ),
               ("DELETE FROM triggers WHERE ScheduleID = %s" ),
               ("DELETE FROM schedules WHERE ScheduleID = %s" )]

    for query in queries:
        cursor.execute(query, (scheduleID,))

    try:
        connection.commit()
    except Exception as e:
        connection.rollback()
        return(jsonify({"error":"Unable to delete schedule", "details":f"{e}"})), 500

    return jsonify({'ScheduleID': scheduleID}), 200

# Function updates schedule of specified ID if user is author and based on input params
def update_schedule(account, cursor, connection, scheduleID, schedule, hubCall=False):
    query = ("SELECT ScheduleID FROM schedules "
                "WHERE AuthorID = %s AND ScheduleID = %s")
    cursor.execute(query, (account['AccountID'], scheduleID,))
    checkID = cursor.fetchone()

    if checkID is None and hubCall is False:
        return({"error": "Forbidden access"}), 401
    
    updateParams = []
    values = []
    newCode = None
    newTriggers = None
    isActive = None
    for key, value in schedule.items():
        if key == "Code":
            newCode = value
            continue
        if key == "Trigger":
            newTriggers = value
            continue
        if not key[0].isupper() or(key in ["Rating","NumRated","ScheduleID","HubID","AuthorID","CopyFrom","HubID","VarDict"]) or value == "":
            continue
        if key == "IsActive":
            isActive = value
            continue
        updateParams.append(f"{key}=%s")
        values.append(value)
    updateParams = ', '.join(updateParams)

    query = (f"UPDATE schedules SET {updateParams} WHERE ScheduleID = %s AND AuthorID = %s")
    values.extend([scheduleID, account['AccountID']])

    try:
        cursor.execute(query, values)
        connection.commit()
    except Exception as e:
        connection.rollback()
        return jsonify({"error" : "Schedule couldn't be updated", "details":f"{e}"}), 500

    query = ("SELECT IsDraft, HubID FROM schedules WHERE ScheduleID = %s")
    cursor.execute(query, (scheduleID,))
    sched = cursor.fetchone()
    draftStatus = sched['IsDraft']
    hubID = sched['HubID']

    if draftStatus+isActive > 1:
        return jsonify({"error" : "Draft Schedule cannot be active"}), 400
    
    if draftStatus == 1:
        isActive = 0

    if isActive is not None:
        query = ("UPDATE schedules SET IsActive = %s WHERE ScheduleID = %s AND AuthorID = %s")
        try:
            cursor.execute(query, (isActive, scheduleID, account['AccountID'],))
            connection.commit()
        except Exception as e:
            connection.rollback()
            return jsonify({"error" : "Schedule couldn't be updated", "details":f"{e}"}), 500

    if newTriggers is not None and newTriggers != []:
        query = ("SELECT TriggerID FROM triggers "
                 "WHERE ScheduleID = %s")
        cursor.execute(query, (scheduleID,))
        trigger = cursor.fetchone()

        if trigger is not None:
            query = ("DELETE FROM trigger_data WHERE TriggerID = %s")
            cursor.execute(query, (trigger['TriggerID'],))

            query = ("DELETE FROM triggers WHERE ScheduleID = %s" )
            try:
                cursor.execute(query, (scheduleID,))
                connection.commit()
            except Exception as e:
                connection.rollback()
                return(jsonify({"error":"Unable to complete update schedule", "details":f"{e}"})), 500
        
        query = ("SELECT TriggerID FROM triggers")
        cursor.execute(query)
        triggers = cursor.fetchall()
        triggers = [trig['TriggerID'] for trig in triggers]
        
        query = ("INSERT INTO triggers (TriggerID, ScheduleID) "
                    "VALUES (%s,%s)")

        triggerID = genRandomID(ids=triggers, prefix='Trg')
        try:
            cursor.execute(query, (triggerID, scheduleID,))
            connection.commit()
        except Exception as e:
            connection.rollback()
            return(jsonify({"error":"Unable to update schedule triggers", "details":f"{e}"})), 500
        
        query = ("INSERT INTO trigger_data (TriggerID, Data, ListPos) "
                    "VALUES ")
        values = ()

        pos = 0
        for v in newTriggers:
            query += ("(%s,%s,%s),")
            values += (triggerID, v,pos,)
            pos += 1
        
        query = query[:-1]
        try:
            cursor.execute(query, values)
            connection.commit()
        except Exception as e:
            connection.rollback()
            return(jsonify({"error":"Unable to update schedule trigger data", "details":f"{e}"})), 500

    if newCode is None:
        return get_schedule_detail(account, cursor, scheduleID)

    queries = [("DELETE FROM function_block_params WHERE ScheduleID = %s" ),
               ("DELETE FROM function_block_links WHERE ScheduleID = %s" ),
               ("DELETE FROM function_blocks WHERE ScheduleID = %s" )]

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
    blockIDs = [blockID['BlockID'] for blockID in blockIDs]

    queries = [("INSERT INTO function_blocks (BlockID, CommandType, Num, ScheduleID) "
                 "VALUES "),
                ("INSERT INTO function_block_links (ParentID, Link, ScheduleID) "
                 "VALUES "),
                ("INSERT INTO function_block_params (Value, FunctionBlockID, ScheduleID, ListPos) "
                 "VALUES ")]
    values = [(), (), ()]
    run = [0,0,0]

    commandTypes = ['FOR', 'WHILE', 'IF', 'ELSE', 'SET', 'WAIT', 'END']
    for funcBlock in newCode:
        run[0] += 1
        if funcBlock.get('CommandType') not in commandTypes:
            return (jsonify({'error':'Invalid argument CommandType must be FOR, WHILE, IF, ELSE, SET; Returning empty Code.'})), 400
        blockID = genRandomID(ids=blockIDs, prefix='Fun')
        blockIDs.append(blockID)

        queries[0] += ("(%s,%s,%s,%s),")
        values[0] += (blockID, funcBlock.get('CommandType'), funcBlock.get('Number'), scheduleID,)

        for link in funcBlock.get('LinkedCommands'):
            run[1] += 1
            queries[1] += ("(%s,%s,%s),")
            values[1] += (blockID, link, scheduleID,)

        pos = 0
        for param in funcBlock.get('Params'):
            run[2] += 1
            queries[2] += ("(%s,%s,%s,%s),")
            values[2] += (param, blockID, scheduleID, pos,)
            pos += 1

    for i in range(3):
        if run[i] == 0:
            continue
        queries[i] = queries[i][:-1]
        try:
            cursor.execute(queries[i], values[i])
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
    try:
        cursor.fetchall()
    except:
        pass

    if request.method == 'GET':
        return get_schedules(account, cursor)
    elif request.method == 'POST':
        return create_schedule(account, cursor, connection, request.json)

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
    try:
        cursor.fetchall()
    except:
        pass

    if request.method == 'GET':
        return get_schedule_detail(account, cursor, scheduleID)
    elif request.method == 'DELETE':
        return delete_schedule(account, cursor, connection, scheduleID)
    elif request.method == 'PATCH':
        return update_schedule(account, cursor, connection, scheduleID, request.json)

    cursor.close()
    connection.close()