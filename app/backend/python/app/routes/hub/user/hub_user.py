from flask import request, jsonify, Blueprint, current_app
from ...accounts import getAccount
from iota import genRandomID

hub_user = Blueprint('hub_user', __name__)

def get_hub_users(account, cursor, HubID):

    query = ("SELECT HubID FROM accounts_hubsRelation WHERE HubID = %s AND AccountID = %s")
    cursor.execute(query, (HubID, account['AccountID']))
    hub = cursor.fetchone()
    if not hub:
        return jsonify({'error': 'User not part of hub'}), 401
    
    
    query = ("SELECT accounts.*, accounts_hubsRelation.PermissionLevel FROM accounts_hubsRelation "
             "JOIN accounts ON accounts_hubsRelation.AccountID = accounts.AccountID "
             "WHERE HubID = %s")
    cursor.execute(query, (HubID,))
    users = cursor.fetchall()

    if not users:
        return jsonify({'error': 'No users found'}), 404

    userList = []
    for user in users:
        userList.append({'AccountID': user['AccountID'], 'Name': user['FirstName'] + " " + user['LastName'], 'PermissionLevel': user['PermissionLevel']})
    userList = sorted(userList, key=lambda x: x['Name'])
    return jsonify(userList), 200