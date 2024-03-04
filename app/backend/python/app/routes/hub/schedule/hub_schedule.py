from flask import request, jsonify, Blueprint, current_app
import json
from ...accounts import getAccount
from iota import genRandomID
from ...schedule.schedule import get_schedule_detail, delete_schedule, create_schedule, update_schedule

hub_schedule = Blueprint('hub_schedule', __name__)

def get_hub_schedules(account, cursor, hubID):
    query = ("SELECT PermissionLevel FROM accounts_hubsRelation WHERE AccountID = %s AND HubID = %s")
    cursor.execute(query, (account['AccountID'], hubID))
    permissionLevel = cursor.fetchone()
    if not permissionLevel:
        return jsonify({'error': 'User not in Hub'}), 401
    permissionLevel = permissionLevel['PermissionLevel']
    
    if permissionLevel == 0:
        return jsonify({'error': 'User does not have permission to view schedules'}), 403
    
    query = ("SELECT ScheduleID, ScheduleName, IsActive, IsDraft, accounts.FirstName, accounts.Surname, PermissionLevel FROM schedules "
             "JOIN accounts ON schedules.AuthorID = accounts.AccountID "
             "JOIN accounts_hubsRelation ON schedules.AuthorID = accounts_hubsRelation.AccountID "
             "WHERE schedules.HubID = %s")
    cursor.execute(query, (hubID,))
    schedules = cursor.fetchall()
    schedules = [{'ScheduleID': schedule['ScheduleID'], 'ScheduleName': schedule['ScheduleName'], 'IsActive': schedule['IsActive'], 'IsDraft': schedule['IsDraft'], 'Author': schedule['FirstName']+" "+schedule['Surname'], 'PermissionLevel': schedule['PermissionLevel']} for schedule in schedules]
    schedules = sorted(schedules, key=lambda x: (x['PermissionLevel'], x['Author'], x['ScheduleName']))
    return jsonify(schedules), 200

def get_one_hub_schedule(account, cursor, hubID, scheduleID):
    query = ("SELECT PermissionLevel FROM accounts_hubsRelation WHERE AccountID = %s AND HubID = %s")
    cursor.execute(query, (account['AccountID'], hubID))
    permissionLevel = cursor.fetchone()['PermissionLevel']
    if not permissionLevel:
        return jsonify({'error': 'User not in Hub'}), 401
    
    if permissionLevel == 0:
        return jsonify({'error': 'User does not have permission to view schedules'}), 403
    
    schedule_details = json.loads(get_schedule_detail(account, cursor, scheduleID, True)[0].data)

    if schedule_details.get('HubID') != hubID:
        return jsonify({'error': 'Schedule not in Hub'}), 403
    
    return jsonify(schedule_details), 200

def add_hub_schedule(account, cursor, connection, hubID, scheduleID):
    query = ("SELECT PermissionLevel FROM accounts_hubsRelation WHERE AccountID = %s AND HubID = %s")
    cursor.execute(query, (account['AccountID'], hubID))
    permissionLevel = cursor.fetchone()['PermissionLevel']
    if not permissionLevel:
        return jsonify({'error': 'User not in Hub'}), 401
    
    if permissionLevel < 3:
        return jsonify({'error': 'User does not have permission to add schedules'}), 403
    
    schedule = json.loads(get_schedule_detail(account, cursor, scheduleID, True)[0].data)
    if schedule.get('error') is not None:
        return jsonify({'error': 'Schedule not found'}), 404

    newID = json.loads(create_schedule(account, cursor, connection, schedule)[0].data).get('ScheduleID')
    schedule['Trigger'] = None

    query = ("UPDATE schedules SET HubID = %s WHERE ScheduleID = %s")
    cursor.execute(query, (hubID, newID))
    return update_schedule(account, cursor, connection, newID, schedule, True)

def remove_hub_schedule(account, cursor, connection, hubID, scheduleID):
    query = ("SELECT PermissionLevel FROM accounts_hubsRelation WHERE AccountID = %s AND HubID = %s")
    cursor.execute(query, (account['AccountID'], hubID))
    permissionLevel = cursor.fetchone()['PermissionLevel']
    if not permissionLevel:
        return jsonify({'error': 'User not in Hub'}), 401
    
    if permissionLevel < 3:
        return jsonify({'error': 'User does not have permission to remove schedules'}), 403
    
    query = ("SELECT ScheduleID FROM schedules WHERE HubID = %s AND ScheduleID = %s")
    cursor.execute(query, (hubID, scheduleID))
    if not cursor.fetchone():
        return jsonify({'error': 'Schedule not in Hub'}), 403

    return delete_schedule(account, cursor, connection, scheduleID, True)

def update_hub_schedule(account, cursor, connection, hubID, scheduleID):
    query = ("SELECT PermissionLevel FROM accounts_hubsRelation WHERE AccountID = %s AND HubID = %s")
    cursor.execute(query, (account['AccountID'], hubID))
    permissionLevel = cursor.fetchone()['PermissionLevel']
    if not permissionLevel:
        return jsonify({'error': 'User not in Hub'}), 401
    
    if permissionLevel < 3:
        return jsonify({'error': 'User does not have permission to update schedules'}), 403
    
    query = ("SELECT ScheduleID FROM schedules WHERE HubID = %s AND ScheduleID = %s")
    cursor.execute(query, (hubID, scheduleID))
    if not cursor.fetchone():
        return jsonify({'error': 'Schedule not in Hub'}), 403

    return update_schedule(account, cursor, connection, scheduleID, request.json, True)

def create_hub_schedule(account, cursor, connection, hubID):
    query = ("SELECT PermissionLevel FROM accounts_hubsRelation WHERE AccountID = %s AND HubID = %s")
    cursor.execute(query, (account['AccountID'], hubID))
    permissionLevel = cursor.fetchone()['PermissionLevel']
    if not permissionLevel:
        return jsonify({'error': 'User not in Hub'}), 401
    
    if permissionLevel < 3:
        return jsonify({'error': 'User does not have permission to create schedules'}), 403
    
    newID = json.loads(create_schedule(account, cursor, connection, request.json)[0].data).get('ScheduleID')

    query = ("UPDATE schedules SET HubID = %s WHERE ScheduleID = %s")
    cursor.execute(query, (hubID, newID))

    return get_schedule_detail(account, cursor, newID, True)

@hub_schedule.route('/hub/<hubID>/schedule', methods=['GET', 'POST'])
def hub_schedule_routes(hubID):
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
        return get_hub_schedules(account, cursor, hubID)
    elif request.method == 'POST':
        return create_hub_schedule(account, cursor, connection, hubID)

@hub_schedule.route('/hub/<hubID>/schedule/<scheduleID>', methods=['GET', 'DELETE', 'PATCH', 'POST'])
def single_hub_schedule_routes(hubID, scheduleID):
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
        return get_one_hub_schedule(account, cursor, hubID, scheduleID)
    elif request.method == 'DELETE':
        return remove_hub_schedule(account, cursor, connection, hubID, scheduleID)
    elif request.method == 'PATCH':
        return update_hub_schedule(account, cursor, connection, hubID, scheduleID)
    elif request.method == 'POST':
        return add_hub_schedule(account, cursor, connection, hubID, scheduleID)