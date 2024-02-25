from flask import request, jsonify, make_response, Blueprint, current_app
from iota import genRandomID

device = Blueprint('device', __name__)

# Function returns list of devices linked to hub
def get_devices(hubID, cursor):
    hubID = request.json.get("HubID")
    query = ("SELECT DeviceID, DeviceName, DeviceType, IpAddress, HubID FROM devices "
                "WHERE HubID = %s")
    
    cursor.execute(query, (hubID,))
    devices = cursor.fetchall()
    return jsonify(devices), 200

def create_device(cursor, connection):
    deviceName = request.json.get("DeviceName")
    deviceType = request.json.get("DeviceType")
    ipAddress = request.json.get("IpAddress")
    hubID = request.json.get("HubID")
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

def get_device_detail(cursor, deviceID):
    query = ("SELECT * FROM devices "
                "WHERE DeviceID = %s")
    cursor.execute(query, (hdeviceID,))
    device = cursor.fetchone()

    if device is None:
        return 404

    details = {'DeviceID': device['DeviceID'],
               'DeviceName': device['DeviceName'],
               'DeviceType': device['DeviceType'],
               'IpAddress': device['IpAddress'],
               'HubID': device['HubID']}
    
    return jsonify(details), 200

Function deletes device of specified ID
def delete_device(hubID, cursor, connection, deviceID):
    query = ("SELECT DeviceID FROM devices "
                "WHERE DeviceID = %s")
    cursor.execute(query, (deviceID,))
    checkExists = cursor.fetchone()

    if checkExists is None:
        return({"error": "device not found"}), 404
    
    query = ("SELECT TriggerID FROM triggers "
                "WHERE DeviceID = %s")
    cursor.execute(query, (deviceID,))
    trigger = cursor.fetchone()

    if trigger is not None:
        return({"error": "device in use"}), 409

    queries = [("DELETE FROM devices WHERE DeviceID = %s" )]
    cursor.execute(query, (deviceID,))

    try:
        connection.commit()
    except:
        connection.rollback()
        return(jsonify({"error":"Unable to delete device", "details":f"{e}"})), 500

    return jsonify(deviceID), 200

# Function updates device of specified ID based on input params
def update_device(cursor, connection, deviceID):
    query = ("SELECT DeviceID FROM devices "
                "WHERE DeviceID = %s")
    cursor.execute(query, deviceID,)
    checkExists = cursor.fetchone()

    if checkExists is None:
        return({"error": "device not found"}), 404
    
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
             
    return get_device_detail(cursor, deviceID)

@device.route("/device" , methods=['POST', 'GET'])
def deviceResponse():

    cursor = current_app.config['cursor']
    connection = current_app.config['connection']

    if request.method == 'GET':
        return get_devices(cursor)
    elif request.method == 'POST':
        return create_device(cursor, connection)

    cursor.close()
    connection.close()

@device.route("/device/<string:deviceID>" , methods=['PATCH', 'DELETE', 'GET'])
def deviceDetails(deviceID):

    cursor = current_app.config['cursor']
    connection = current_app.config['connection']

    if request.method == 'GET':
        return get_device_detail(cursor, deviceID)
    elif request.method == 'DELETE':
        return delete_device(cursor, connection, deviceID)
    elif request.method == 'PATCH':
        return update_device(cursor, connection, deviceID)

    cursor.close()
    connection.close()