from flask import request, jsonify, Blueprint, current_app
from ...accounts import getAccount
from iota import genRandomID

device = Blueprint('device', __name__)
EditPermLevel = 3
ViewPermLevel = 1

# Function returns list of devices linked to hub
def get_devices(account, cursor, HubID):
    hubID = HubID
    
    query = ("SELECT * FROM accounts_hubsRelation "
                "WHERE AccountID = %s AND HubID = %s")
    cursor.execute(query, (account['AccountID'], hubID,))
    checkPerm = cursor.fetchone()

    if checkPerm is None or checkPerm['PermissionLevel'] < ViewPermLevel:
        return({"error": "Forbidden access"}), 403
    
    query = ("SELECT DeviceID, DeviceName, Company FROM devices "
                "WHERE HubID = %s ORDER BY DeviceName ASC")

    cursor.execute(query, (hubID,))
    devices = cursor.fetchall()

    devices = [{k: v for k, v in device.items()} for device in devices]
    for device in devices:
        device['Vars'] = get_device_vars(cursor, device['DeviceID'])

    return jsonify(devices), 200

def get_device_vars(cursor, deviceID):
    query = ("SELECT * FROM device_vars "
                "WHERE DeviceID = %s")
    cursor.execute(query, (deviceID,))
    vars = cursor.fetchall()
    deviceVars = {}
    for var in vars:
        deviceVars[var['VarName']] = var['VarType']
    return deviceVars

def create_device(account, cursor, connection, hubID):
    query = ("SELECT * FROM accounts_hubsRelation "
                "WHERE AccountID = %s AND HubID = %s")
    cursor.execute(query, (account['AccountID'], hubID,))
    checkPerm = cursor.fetchone()

    if checkPerm is None or checkPerm['PermissionLevel'] < EditPermLevel:
        return({"error": "Forbidden access"+hubID}), 403
    
    thisID = request.json.get('DeviceID')

    query = ("INSERT INTO devices (DeviceID, `Key`, DeviceName, Company, Version, IpAddress, HubID) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    try:
        cursor.execute(query, (thisID, request.json.get('Key'), request.json.get('DeviceName'), request.json.get('Company'), request.json.get('Version'), request.json.get('IpAddress'), hubID,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({'DeviceID':thisID}), 200

def get_device_detail(account, cursor, deviceID, hubID):
    query = ("SELECT * FROM accounts_hubsRelation "
                "WHERE AccountID = %s AND HubID = %s")
    cursor.execute(query, (account['AccountID'], hubID,))
    checkPerm = cursor.fetchone()

    if checkPerm is None or checkPerm['PermissionLevel'] < ViewPermLevel:
        return({"error": "Forbidden access"}), 403

    query = ("SELECT * FROM devices "
                "WHERE DeviceID = %s AND HubID = %s")
    cursor.execute(query, (deviceID, hubID,))
    device = cursor.fetchone()
    device = {k: v for k, v in device.items()}
    device['Vars'] = get_device_vars(cursor, deviceID)

    if device is None:
        return({"error": "device not found"}), 404
    
    return jsonify(device), 200

#Function deletes device of specified ID
def delete_device(account, cursor, connection, deviceID, hubID):
    query = ("SELECT * FROM devices "
                "JOIN accounts_hubsRelation ON devices.HubID = accounts_hubsRelation.HubID "
                "WHERE devices.DeviceID = %s AND devices.HubID = %s AND accounts_hubsRelation.AccountID = %s")
    cursor.execute(query, (deviceID, hubID, account['AccountID'],))
    checkExists = cursor.fetchone()

    if checkExists is None or checkExists['PermissionLevel'] < EditPermLevel:
        return({"error": "Forbidden access"}), 403
    
    query = ("SELECT * FROM trigger_data "
                "WHERE DeviceID = %s")
    cursor.execute(query, (deviceID,))
    trigger = cursor.fetchall()

    if len(trigger) > 0:
        return({"error": f"device in use at {trigger}"}), 409

    query = ("DELETE FROM devices WHERE DeviceID = %s" )
    cursor.execute(query, (deviceID,))

    try:
        connection.commit()
    except Exception as e:
        connection.rollback()
        return(jsonify({"error":"Unable to delete device", "details":f"{e}"})), 500

    return jsonify({'DeviceID': deviceID}), 200

# Function updates device of specified ID based on input params
def update_device(account, cursor, connection, deviceID, hubID):
    query = ("SELECT * FROM devices "
                "JOIN accounts_hubsRelation ON devices.HubID = accounts_hubsRelation.HubID "
                "WHERE devices.DeviceID = %s AND devices.HubID = %s AND accounts_hubsRelation.AccountID = %s")
    cursor.execute(query, (deviceID, hubID, account['AccountID'],))
    checkExists = cursor.fetchone()

    if checkExists is None or checkExists['PermissionLevel'] < EditPermLevel:
        return({"error": "Forbidden access"}), 403
    
    updateParams = []
    values = []
    for key, value in request.json.items():
        if not key[0].isupper() or key == "HubID":
            continue
        if value == "":
            continue
        updateParams.append(f"`{key}`=%s")
        values.append(value)
    updateParams = ', '.join(updateParams)

    query = (f"UPDATE devices SET {updateParams} WHERE DeviceID = %s")
    values.extend([deviceID,])

    try:
        cursor.execute(query, values)
        connection.commit()
    except Exception as e:
        connection.rollback()
        return jsonify({"error" : "Device couldn't be updated", "details":f"{e}"}), 500
             
    return get_device_detail(account, cursor, deviceID, hubID)

@device.route("/hub/<string:hubID>/device" , methods=['POST', 'GET'])
def deviceResponse(hubID):
    #Get current user info
    account = getAccount()
    if account is None:
        return jsonify({"error": "Session ID is invalid"}), 401

    cursor = current_app.config['cursor']
    connection = current_app.config['connection']

    if request.method == 'GET':
        return get_devices(account, cursor, hubID)
    elif request.method == 'POST':
        return create_device(account, cursor, connection, hubID)

    cursor.close()
    connection.close()

@device.route("/hub/<string:hubID>/device/<string:deviceID>" , methods=['PATCH', 'DELETE', 'GET'])
def deviceDetails(hubID,deviceID):
    #Get current user info
    account = getAccount()
    if account is None:
        return jsonify({"error": "Session ID is invalid"}), 401

    cursor = current_app.config['cursor']
    connection = current_app.config['connection']

    if request.method == 'GET':
        return get_device_detail(account, cursor, deviceID, hubID)
    elif request.method == 'DELETE':
        return delete_device(account, cursor, connection, deviceID, hubID)
    elif request.method == 'PATCH':
        return update_device(account, cursor, connection, deviceID, hubID)

    cursor.close()
    connection.close()
