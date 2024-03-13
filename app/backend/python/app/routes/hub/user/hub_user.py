from flask import request, jsonify, Blueprint, current_app
from ...accounts import getAccount
from iota import genRandomID
import time

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
        userList.append({'AccountID': user['AccountID'], 'Name': user['FirstName'] + " " + user['Surname'], 'PermissionLevel': user['PermissionLevel']})
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
    
    query = ("SELECT PermissionLevel FROM accounts_hubsRelation WHERE HubID = %s AND AccountID = %s")
    cursor.execute(query, (hubID, accountID))
    user = cursor.fetchone()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if hub['PermissionLevel'] <= user['PermissionLevel']:
        return jsonify({'error': 'User does not have permission to manage users with higher or equal permission levels'}), 403

    query = ("DELETE FROM accounts_hubsRelation WHERE HubID = %s AND AccountID = %s")
    try:
        cursor.execute(query, (hubID, accountID))
        current_app.config['connection'].commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'HubID': hubID, 'AccountID': accountID}), 200

def manage_hub_user(account, cursor, connection, hubID, accountID):
    query = ("SELECT PermissionLevel FROM accounts_hubsRelation WHERE HubID = %s AND AccountID = %s")
    cursor.execute(query, (hubID, account['AccountID']))
    hub = cursor.fetchone()
    if not hub:
        return jsonify({'error': 'User not part of hub'}), 401

    if hub['PermissionLevel'] < 4:
        return jsonify({'error': 'User does not have permission to manage users in hub'}), 403
    
    query = ("SELECT PermissionLevel FROM accounts_hubsRelation WHERE HubID = %s AND AccountID = %s")
    cursor.execute(query, (hubID, accountID))
    user = cursor.fetchone()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    permissionLevel = request.json.get('PermissionLevel')
    if permissionLevel < 0 or permissionLevel > 5:
        return jsonify({'error': 'Invalid permission level'}), 400
    
    if hub['PermissionLevel'] <= user['PermissionLevel'] and hub['PermissionLevel'] != 5:
        return jsonify({'error': 'User does not have permission to manage users with higher or equal permission levels'}), 403
    
    if permissionLevel > hub['PermissionLevel']:
        return jsonify({'error': 'User cannot set permission level higher than their own'}), 403

    query = ("UPDATE accounts_hubsRelation SET PermissionLevel = %s WHERE HubID = %s AND AccountID = %s")
    try:
        cursor.execute(query, (permissionLevel, hubID, accountID))
        connection.commit()
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

    return jsonify({'AccountID': user['AccountID'], 'Name': user['FirstName'] + " " + user['Surname'], 'PermissionLevel': user['PermissionLevel']}), 200

def create_invite_token(account, cursor, connection, hubID):
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

    token = genRandomID(40, tokens, 'Inv')
    query = ("INSERT INTO hub_inviteTokens (HubID, Token, Expiry) VALUES (%s, %s, %s)")
    expiry = int(time.time() + 86400)
    try:
        cursor.execute(query, (hubID, token, expiry))
        connection.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'HubID': hubID, 'Token': token}), 200

def accept_hub_invite(account, cursor, connection, token):
    query = ("SELECT HubID FROM hub_inviteTokens WHERE Token = %s")
    cursor.execute(query, (token,))
    hub = cursor.fetchone()
    if not hub:
        return jsonify({'error': 'Token not found'}), 404

    query = ("INSERT INTO accounts_hubsRelation (AccountID, HubID, PermissionLevel) VALUES (%s,%s,%s)")
    try:
        cursor.execute(query, (account['AccountID'], hub['HubID'], 1))
        connection.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'HubID': hub['HubID']}), 200

def clear_expired_tokens(cursor, connection):
    query = ("DELETE FROM hub_inviteTokens WHERE Expiry < %s")
    try:
        cursor.execute(query, (int(time.time()),))
        connection.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def force_add_to_hub(cursor, connection, hubID):
    accountID = request.json.get('AccountID')
    permmissionLevel = request.json.get('PermissionLevel')
    query = ("INSERT INTO accounts_hubsRelation (AccountID, HubID, PermissionLevel) VALUES (%s,%s,%s)")
    try:
        cursor.execute(query, (accountID, hubID, permmissionLevel))
        connection.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'AccountID': accountID, 'PermissionLevel': permmissionLevel}), 200
    
def leave_hub(cursor, connection, account, hubID):
    query = ("DELETE FROM accounts_hubsRelation WHERE AccountID = %s AND HubID = %s")
    try:
        cursor.execute(query, (account['AccountID'], hubID))
        connection.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'HubID': hubID}), 200

@hub_user.route('/hub/<hubID>/user', methods=['GET', 'POST', 'DELETE'])
def hub_get_users_route(hubID):
    account = getAccount()
    if account is None:
        return jsonify({'error': 'Session ID is invalid'}), 401

    cursor = current_app.config['cursor']
    connection = current_app.config['connection']

    try:
        cursor.fetchall()
    except:
        pass

    clear_expired_tokens(cursor, connection)
    if request.method == 'GET':
        return get_hub_users(account, cursor, hubID)
    elif request.method == 'POST':
        return force_add_to_hub(cursor, connection, hubID)
    else:
        return leave_hub(cursor, connection, account, hubID)

@hub_user.route('/hub/<hubID>/user/<accountID>', methods=['DELETE', 'PATCH', 'GET'])
def hub_user_route(hubID, accountID):
    account = getAccount()
    if account is None:
        return jsonify({'error': 'Session ID is invalid'}), 401

    cursor = current_app.config['cursor']
    connection = current_app.config['connection']

    try:
        cursor.fetchall()
    except:
        pass

    clear_expired_tokens(cursor, connection)
    if request.method == 'DELETE':
        return remove_hub_user(account, cursor, hubID, accountID)
    elif request.method == 'PATCH':
        return manage_hub_user(account, cursor, connection, hubID, accountID)
    else:
        return get_one_hub_user(account, cursor, hubID, accountID)

@hub_user.route('/hub/<hubID>/invite', methods=['POST'])
def hub_invite_route(hubID):
    account = getAccount()
    if account is None:
        return jsonify({'error': 'Session ID is invalid'}), 401

    cursor = current_app.config['cursor']
    connection = current_app.config['connection']

    try:
        cursor.fetchall()
    except:
        pass

    clear_expired_tokens(cursor, connection)
    return create_invite_token(account, cursor, connection, hubID)

@hub_user.route('/hub/invite/<token>', methods=['POST'])
def join_hub_route(token):
    account = getAccount()
    if account is None:
        return jsonify({'error': 'Session ID is invalid'}), 401

    cursor = current_app.config['cursor']
    connection = current_app.config['connection']

    try:
        cursor.fetchall()
    except:
        pass

    clear_expired_tokens(cursor, connection)
    return accept_hub_invite(account, cursor, connection, token)
