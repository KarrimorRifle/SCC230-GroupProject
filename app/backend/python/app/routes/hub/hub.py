from flask import request, jsonify, Blueprint, current_app
from ..accounts import getAccount
from iota import genRandomID

hub = Blueprint('hub', __name__)

# Function returns list of hubs linked to user who is logged in
def get_hubs(account, cursor):
    query = ("SELECT accounts_hubsRelation.PermissionLevel, hubs.*, "
             "(SELECT COUNT(AccountID) "
             "FROM accounts_hubsRelation " 
             "WHERE accounts_hubsRelation.HubID = hubs.HubID) AS UserCount "
             "FROM accounts_hubsRelation "
             "JOIN hubs ON accounts_hubsRelation.HubID = hubs.HubID "
             "WHERE AccountID = %s AND accounts_hubsRelation.PermissionLevel > 0 "
             "ORDER BY HubName")
    
    cursor.execute(query, (account['AccountID'],))
    hubs = cursor.fetchall()

    return jsonify(hubs), 200

# Function returns one hub linked to user specified by hubID in url
def get_one_hub(account, cursor, hubID):
    query = ("SELECT * FROM accounts_hubsRelation "
             "WHERE AccountID = %s AND HubID = %s")
    cursor.execute(query, (account['AccountID'], hubID,))
    hub = cursor.fetchone()

    if hub is None:
        return jsonify({"error": "Hub not found"}), 404
    
    permLevel = hub['PermissionLevel']

    if permLevel < 1:
        return jsonify({"error": "Permission denied"}), 403

    query = ("SELECT * FROM hubs WHERE HubID = %s")
    cursor.execute(query, (hubID,))
    hub = cursor.fetchone()
    return jsonify({'HubID':hub['HubID'], 'HubName':hub['HubName'], 'PermissionLevel': permLevel}), 200

# Function creates new hub and links it to user who is logged in
def create_hub(account, cursor, connection):
    hubName = request.json.get("HubName")
    query = ("SELECT HubID FROM hubs")
    cursor.execute(query)
    hubIDs = cursor.fetchall()
    thisID = genRandomID(ids=hubIDs, prefix='Hub')
    query = ("INSERT INTO hubs (HubID, HubName) "
                     "VALUES (%s,%s)")
    try:
        cursor.execute(query, (thisID, hubName,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 500
    
    query = ("INSERT INTO accounts_hubsRelation (AccountID, HubID, PermissionLevel) VALUES (%s,%s,%s)")
    try:
        cursor.execute(query, (account['AccountID'], thisID, 5))
        connection.commit()
    except Exception as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({'HubID':thisID}), 200

# Function deletes hub and all its relations with accounts
def delete_hub(account, cursor, connection, hubID):
    query = ("SELECT * FROM accounts_hubsRelation "
             "WHERE AccountID = %s AND HubID = %s")
    cursor.execute(query, (account['AccountID'], hubID,))
    hub = cursor.fetchone()

    if hub is None:
        return jsonify({"error": "Hub not found"}), 404
    
    if hub['PermissionLevel'] < 5:
        return jsonify({"error": "Permission denied"}), 403

    query = ("DELETE FROM hubs WHERE HubID = %s")
    cursor.execute(query, (hubID,))
    connection.commit()
    return jsonify({'HubID':hubID}), 200

# Function updates hub name (only name can be updated in hubs)
def update_hub(account, cursor, connection, hubID):
    hubName = request.json.get("HubName")
    query = ("SELECT * FROM accounts_hubsRelation "
             "WHERE AccountID = %s AND HubID = %s")
    cursor.execute(query, (account['AccountID'], hubID,))
    hub = cursor.fetchone()

    if hub is None:
        return jsonify({"error": "Hub not found"}), 404
    
    permLevel = hub['PermissionLevel']
    
    if permLevel < 5:
        return jsonify({"error": "Permission denied"}), 403

    query = ("UPDATE hubs SET HubName = %s WHERE HubID = %s")
    cursor.execute(query, (hubName, hubID,))
    connection.commit()
    return jsonify({'HubID': hubID, 'HubName': hubName, 'PermissionLevel': permLevel}), 200

@hub.route('/hub', methods=['GET', 'POST'])
def hub_route():
    #Get current user info
    account = getAccount()
    if account is None:
        return jsonify({"error": "Session ID is invalid"}), 401

    cursor = current_app.config['cursor']
    connection = current_app.config['connection']
    cursor.fetchall()

    if request.method == 'GET':
        return get_hubs(account, cursor)
    elif request.method == 'POST':
        return create_hub(account, cursor, connection)
    
@hub.route('/hub/<string:hubID>', methods=['GET', 'DELETE', 'PATCH'])
def single_hub_route(hubID):
    #Get current user info
    account = getAccount()
    if account is None:
        return jsonify({"error": "Session ID is invalid"}), 401

    cursor = current_app.config['cursor']
    connection = current_app.config['connection']
    cursor.fetchall()

    if request.method == 'GET':
        return get_one_hub(account, cursor, hubID)
    elif request.method == 'DELETE':
        return delete_hub(account, cursor, connection, hubID)
    elif request.method == 'PATCH':
        return update_hub(account, cursor, connection, hubID)
