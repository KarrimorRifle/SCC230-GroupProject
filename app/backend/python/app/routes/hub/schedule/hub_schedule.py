from flask import request, jsonify, Blueprint, current_app
from ...accounts import getAccount
from iota import genRandomID

hub_schedule = Blueprint('hub_schedule', __name__)

def get_hub_schedules(account, cursor, hubID):
    query = ("SELECT PermissionLevel FROM accounts_hubsRelations WHERE AccountID = %s AND HubID = %s")
    cursor.execute(query, (account['AccountID'], hubID))
    permissionLevel = cursor.fetchone()['PermissionLevel']
    if not permissionLevel:
        return jsonify({'error': 'User not in Hub'}), 401
    
    if permissionLevel == 0:
        return jsonify({'error': 'User does not have permission to view schedules'}), 403
    
    query = ("SELECT ScheduleID, ScheduleName, IsActive, accounts.FirstName, accounts.Surname, PermissionLevel FROM schedules "
             "JOIN accounts ON schedules.AuthorID = accounts.AccountID "
             "JOIN accounts_hubsRelations ON schedules.AuthorID = accounts_hubsRelations.AccountID "
             "WHERE schedules.HubID = %s")
    cursor.execute(query, (hubID,))
    schedules = cursor.fetchall()
    schedules = [{'ScheduleID': schedule['ScheduleID'], 'ScheduleName': schedule['ScheduleName'], 'IsActive': schedule['IsActive'], 'Author': schedule['FirstName']+" "+schedule['Surname'], 'PermissionLevel': schedule['PermissionLevel']} for schedule in schedules]
    schedules = sorted(schedules, x=lambda x: (x['PermissionLevel'], x['Author'], x['ScheduleName']))
    return jsonify(schedules), 200