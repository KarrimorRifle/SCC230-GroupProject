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

def manage_hub_user(account, cursor, hubID, accountID):
    query = ("SELECT PermissionLevel FROM accounts_hubsRelation WHERE HubID = %s AND AccountID = %s")
    cursor.execute(query, (hubID, account['AccountID']))
    hub = cursor.fetchone()
    if not hub:
        return jsonify({'error': 'User not part of hub'}), 401

    if hub['PermissionLevel'] < 4:
        return jsonify({'error': 'User does not have permission to manage users in hub'}), 403

    permissionLevel = request.json.get('PermissionLevel')
    if permissionLevel < 0 or permissionLevel > 5:
        return jsonify({'error': 'Invalid permission level'}), 400
    
    if permissionLevel < hub['PermissionLevel']:
        return jsonify({'error': 'User cannot set permission level higher than their own'}), 403

    query = ("UPDATE accounts_hubsRelation SET PermissionLevel = %s WHERE HubID = %s AND AccountID = %s")
    try:
        cursor.execute(query, (permissionLevel, hubID, accountID))
        current_app.config['connection'].commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'HubID': hubID, 'AccountID': accountID, 'PermissionLevel': permissionLevel}), 200

def get_one_hub_user(account, cursor, hubID, accountID):
    query = ("SELECT PermissionLevel FROM accounts_hubsRelation WHERE HubID = %s AND AccountID = %s")
    cursor.execute(query, (hubID, account['AccountID']))
    hub = cursor.fetchone()
    if not hub:
        return jsonify({'error': 'User not part of hub'}), 401

    if hub['PermissionLevel'] < 4:
        return jsonify({'error': 'User does not have permission to access specific users in hub'}), 403

    query = ("SELECT accounts.*, accounts_hubsRelation.PermissionLevel FROM accounts_hubsRelation "
             "JOIN accounts ON accounts_hubsRelation.AccountID = accounts.AccountID "
             "WHERE HubID = %s AND accounts.AccountID = %s")
    cursor.execute(query, (hubID, accountID))
    user = cursor.fetchone()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'AccountID': user['AccountID'], 'Name': user['FirstName'] + " " + user['LastName'], 'PermissionLevel': user['PermissionLevel']}), 200

def create_invite_token(account, cursor, hubID):
    query = ("SELECT PermissionLevel FROM accounts_hubsRelation WHERE HubID = %s AND AccountID = %s")
    cursor.execute(query, (hubID, account['AccountID']))
    hub = cursor.fetchone()
    if not hub:
        return jsonify({'error': 'User not part of hub'}), 401

    if hub['PermissionLevel'] < 4:
        return jsonify({'error': 'User does not have permission to create invite tokens for hub'}), 403

    query = ("SELECT Token FROM hub_inviteTokens WHERE HubID = %s")
    cursor.execute(query, (hubID,))
    tokens = cursor.fetchall()
    tokens = [token['Token'] for token in tokens]

    # ADD TOKEN EXPIRATION DATE AND IMPLEMENT
    token = genRandomID(40, tokens, 'Inv')
    query = ("INSERT INTO hub_inviteTokens (HubID, Token) VALUES (%s, %s)")
    try:
        cursor.execute(query, (hubID, token))
        current_app.config['connection'].commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'HubID': hubID, 'Token': token}), 200