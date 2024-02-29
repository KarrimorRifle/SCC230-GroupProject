from flask import request, jsonify, Blueprint, current_app
from ...accounts import getAccount
from iota import genRandomID

hub_user = Blueprint('hub_user', __name__)

def get_hub_users(account, cursor, hubID):

    query = ("SELECT HubID FROM accounts_hubsRelation WHERE HubID = %s AND AccountID = %s")
    cursor.execute(query, (hubID, account['AccountID']))
    hub = cursor.fetchone()
    if not hub:
        return jsonify({'error': 'User not part of hub'}), 401
    
    
    query = ("SELECT accounts.*, accounts_hubsRelation.PermissionLevel FROM accounts_hubsRelation "
             "JOIN accounts ON accounts_hubsRelation.AccountID = accounts.AccountID "
             "WHERE HubID = %s")
    cursor.execute(query, (hubID,))
    users = cursor.fetchall()

    if not users:
        return jsonify({'error': 'No users found'}), 404

    userList = []
    for user in users:
        userList.append({'AccountID': user['AccountID'], 'Name': user['FirstName'] + " " + user['LastName'], 'PermissionLevel': user['PermissionLevel']})
    userList = sorted(userList, key=lambda x: (x['PermissionLevel'], x['Name']))
    return jsonify(userList), 200

def remove_hub_user(account, cursor, hubID, accountID):
    query = ("SELECT PermissionLevel FROM accounts_hubsRelation WHERE HubID = %s AND AccountID = %s")
    cursor.execute(query, (hubID, account['AccountID']))
    hub = cursor.fetchone()
    if not hub:
        return jsonify({'error': 'User not part of hub'}), 401

    if hub['PermissionLevel'] < 4:
        return jsonify({'error': 'User does not have permission to remove users from hub'}), 403

    query = ("DELETE FROM accounts_hubsRelation WHERE HubID = %s AND AccountID = %s")
    try:
        cursor.execute(query, (hubID, accountID))
        current_app.config['connection'].commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'HubID': hubID, 'AccountID': accountID}), 200