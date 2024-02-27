from flask import request, jsonify, make_response, Blueprint, current_app
from .accounts import getAccount
from iota import genRandomID

device = Blueprint('device', __name__)
editPermLevel = 2

# Function returns list of devices linked to hub
def get_devices(account, cursor):
    hubID = request.json.get("HubID")
    query = ("SELECT DeviceID, DeviceName, DeviceType FROM devices "
                "WHERE HubID = %s")
    
    cursor.execute(query, (hubID,))
    devices = cursor.fetchall()
    return jsonify(devices), 200

def create_device(account, cursor, connection):
    deviceName = request.json.get("DeviceName")
    deviceType = request.json.get("DeviceType")
    ipAddress = request.json.get("IpAddress")
    hubID = request.json.get("HubID")

    query = ("SELECT * FROM accounts_hubsRelation "
                "WHERE AccountID = %s AND HubID = %s")
    cursor.execute(query, (account['AccountID'], hubID,))
    checkPerm = cursor.fetchone()

    if checkPerm is None or checkPerm['PermissionLevel'] < editPermLevel:
        return({"error": "Forbidden access"}), 401
    
    query = ("SELECT DeviceID FROM devices")
    cursor.execute(query)
    deviceIDs = cursor.fetchall()
    thisID = genRandomID(ids=deviceIDs, prefix='Dev')
    query = ("INSERT INTO devices (DeviceID, DeviceName, DeviceType, IpAddress, HubID) "
                     "VALUES (%s,%s,%s,%s,%s)")
    try:
        cursor.execute(query, (thisID, deviceName, deviceType, ipAddress, hubID,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({'DeviceID':thisID}), 200

def get_device_detail(account, cursor, deviceID):
    query = ("SELECT * FROM devices "
                "WHERE DeviceID = %s")
    cursor.execute(query, (deviceID,))
    device = cursor.fetchone()

    if device is None:
        return 404

    details = {'DeviceID': device['DeviceID'],
               'DeviceName': device['DeviceName'],
               'DeviceType': device['DeviceType'],
               'IpAddress': device['IpAddress'],
               'HubID': device['HubID']}
    
    return jsonify(details), 200

#Function deletes device of specified ID
def delete_device(account, cursor, connection, deviceID):
    query = ("SELECT * FROM devices "
                "WHERE DeviceID = %s")
    cursor.execute(query, (deviceID,))
    checkExists = cursor.fetchone()

    if checkExists is None:
        return({"error": "device not found"}), 404
    
    query = ("SELECT * FROM accounts_hubsRelation "
                "WHERE AccountID = %s AND HubID = %s")
    cursor.execute(query, (account['AccountID'], checkExists['HubID'],))
    checkPerm = cursor.fetchone()

    if checkPerm is None or checkPerm['PermissionLevel'] < editPermLevel:
        return({"error": "Forbidden access"}), 401
    
    query = ("SELECT * FROM trigger_data "
                "WHERE DeviceID = %s")
    cursor.execute(query, (deviceID,))
    trigger = cursor.fetchall()

    if trigger != []:
        return({"error": "device in use"}), 409

    query = ("DELETE FROM devices WHERE DeviceID = %s" )
    cursor.execute(query, (deviceID,))

    try:
        connection.commit()
    except Exception as e:
        connection.rollback()
        return(jsonify({"error":"Unable to delete device", "details":f"{e}"})), 500

    return jsonify(deviceID), 200

# Function updates device of specified ID based on input params
def update_device(account, cursor, connection, deviceID):
    query = ("SELECT * FROM devices "
                "WHERE DeviceID = %s")
    cursor.execute(query, (deviceID,))
    checkExists = cursor.fetchone()

    if checkExists is None:
        return({"error": "device not found"}), 404
    
    query = ("SELECT * FROM accounts_hubsRelation "
                "WHERE AccountID = %s AND HubID = %s")
    cursor.execute(query, (account['AccountID'], checkExists['HubID'],))
    checkPerm = cursor.fetchone()

    if checkPerm is None or checkPerm['PermissionLevel'] < editPermLevel:
        return({"error": "Forbidden access"}), 401
    
    updateParams = []
    values = []
    for key, value in request.json.items():
        if not key[0].isupper():
            continue
        if value == "":
            continue
        updateParams.append(f"{key}=%s")
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
             
    return get_device_detail(account, cursor, deviceID)

@device.route("/device" , methods=['POST', 'GET'])
def deviceResponse():
    #Get current user info
    account = getAccount()
    if account is None:
        return jsonify({"error": "Session ID is invalid"}), 401

    cursor = current_app.config['cursor']
    connection = current_app.config['connection']

    if request.method == 'GET':
        return get_devices(account, cursor)
    elif request.method == 'POST':
        return create_device(account, cursor, connection)

    cursor.close()
    connection.close()

@device.route("/device/<string:deviceID>" , methods=['PATCH', 'DELETE', 'GET'])
def deviceDetails(deviceID):
    #Get current user info
    account = getAccount()
    if account is None:
        return jsonify({"error": "Session ID is invalid"}), 401

    cursor = current_app.config['cursor']
    connection = current_app.config['connection']

    if request.method == 'GET':
        return get_device_detail(account, cursor, deviceID)
    elif request.method == 'DELETE':
        return delete_device(account, cursor, connection, deviceID)
    elif request.method == 'PATCH':
        return update_device(account, cursor, connection, deviceID)

    cursor.close()
    connection.close()