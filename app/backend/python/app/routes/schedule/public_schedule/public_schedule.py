from flask import request, jsonify, Blueprint, current_app
from ...accounts import getAccount
import json
from ..schedule import get_schedule_detail, create_schedule, update_schedule

public_schedule = Blueprint('public_schedule', __name__)

def get_one_public_schedule(account, cursor, scheduleID):
    cursor = current_app.config['cursor']
    return get_schedule_detail(account, cursor, scheduleID, True)

def save_public_schedule(account, cursor, connection, scheduleID):
    query = ("SELECT IsPublic FROM schedules WHERE ScheduleID = %s")
    cursor.execute(query, (scheduleID,))
    isPublic = cursor.fetchone()['IsPublic']

    if isPublic == 0:
        return jsonify({'error': 'Schedule is not public'}), 403

    schedule = json.loads(get_schedule_detail(account, cursor, scheduleID, True)[0].data)
    if schedule.get('error') is not None:
        return jsonify({'error': schedule['error']}), 404

    newID = json.loads(create_schedule(account, cursor, connection, schedule)[0].data).get('ScheduleID')

    copyFrom = schedule.get('CopyFrom')
    if copyFrom is None:
        copyFrom = schedule['AuthorID']

    query = ("UPDATE schedules SET IsPublic = 0, AuthorID = %s, CopyFrom = %s WHERE ScheduleID = %s")
    schedule['IsPublic'] = 0
    cursor.execute(query, (account['AccountID'], copyFrom, newID))
    try:
        connection.commit()
    except:
        return jsonify({'error': 'Error updating schedule'}), 500

    return update_schedule(account, cursor, connection, newID, schedule, True)

def save_public_schedule_to_hub(account, cursor, connection, hubID, scheduleID):
    newID = json.loads(save_public_schedule(account, cursor, connection, scheduleID)[0].data).get('ScheduleID')

    query = ("UPDATE schedules SET HubID = %s WHERE ScheduleID = %s")
    cursor.execute(query, (hubID, newID))
    try:
        connection.commit()
    except:
        return jsonify({'error': 'Error updating schedule'}), 500
    
    return get_schedule_detail(account, cursor, newID, True)

def rate_public_schedule(account, cursor, connection, scheduleID):
    query = ("SELECT IsPublic, NumRated, Rating FROM schedules WHERE ScheduleID = %s")
    cursor.execute(query, (scheduleID,))
    schedule = cursor.fetchone()

    if schedule is None:
        return jsonify({'error': 'Schedule is not found'}), 404

    isPublic = schedule['IsPublic']
    numRated = schedule['NumRated']
    rating = schedule['Rating']

    if isPublic == 0:
        return jsonify({'error': 'Schedule is not public'}), 403

    if account is None:
        return jsonify({'error': 'User not logged in'}), 401
    
    newRating = request.json.get('Rating')
    if newRating is None:
        return jsonify({'error': 'No rating provided'}), 400
    
    try:
        newRating = int(newRating)
        if newRating < 0 or newRating > 5:
            return jsonify({'error': 'Rating must be between 0 and 5'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid rating format'}), 400
    
    newRating = int(((rating * numRated) + int(newRating)) / (numRated + 1))
    numRated += 1

    query = ("UPDATE schedules SET Rating = %s, NumRated = %s WHERE ScheduleID = %s")
    cursor.execute(query, (newRating, numRated, scheduleID))
    try:
        connection.commit()
    except:
        return jsonify({'error': 'Error updating rating'}), 500
    
    return jsonify({'ScheduleID': scheduleID, 'Rating': newRating}), 200

@public_schedule.route('/schedule/public', methods=['GET'])
def get_public_schedules():
    cursor = current_app.config['cursor']

    cursor.execute("SELECT ScheduleID, ScheduleName, IsActive, IsPublic, Rating, IsDraft, CopyFrom FROM schedules WHERE IsPublic = 1 "
                   "ORDER BY Rating DESC, ScheduleName ASC")
    schedules = cursor.fetchall()

    return jsonify(schedules), 200

@public_schedule.route('/schedule/public/<string:scheduleID>', methods=['GET', 'POST', 'PATCH'])
def single_public_schedule_routes(scheduleID):
    cursor = current_app.config['cursor']
    connection = current_app.config['connection']
    account = getAccount()

    if request.method == 'GET':
        return get_one_public_schedule(account, cursor, scheduleID)
    elif request.method == 'POST':
        return save_public_schedule(account, cursor, connection, scheduleID)
    elif request.method == 'PATCH':
        return rate_public_schedule(account, cursor, connection, scheduleID)
    
@public_schedule.route('/hub/<string:hubID>/schedule/public/<string:scheduleID>', methods=['POST'])
def public_hub_schedule_routes(hubID, scheduleID):
    cursor = current_app.config['cursor']
    connection = current_app.config['connection']
    account = getAccount()

    return save_public_schedule_to_hub(account, cursor, connection, hubID, scheduleID)
