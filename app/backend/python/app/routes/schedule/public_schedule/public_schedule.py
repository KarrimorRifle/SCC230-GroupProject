from flask import request, jsonify, Blueprint, current_app
from ...accounts import getAccount
from schedule import get_schedule_detail

public_schedule = Blueprint('public_schedule', __name__)

def get_one_public_schedule(account, cursor, scheduleID):
    cursor = current_app.config['cursor']
    return get_schedule_detail(account, cursor, scheduleID, True)

def save_public_schedule(account, cursor, connection, scheduleID):
    pass

@public_schedule.route('/schedule/public', methods=['GET'])
def get_public_schedules():
    cursor = current_app.config['cursor']

    cursor.execute("SELECT ScheduleID, ScheduleName, IsActive, IsPublic, Rating, IsDraft FROM schedules WHERE IsPublic = 1")
    schedules = [schedule for schedule in cursor.fetchall()]
    schedules = sorted(schedules, key=lambda x: (-x['Rating'], x['ScheduleName']), reverse=True)
    return jsonify(schedules), 200

@public_schedule.route('/schedule/public/<string:scheduleID>', methods=['GET', 'POST', 'PATCH'])
def single_public_schedule_routes(scheduleID):
    cursor = current_app.config['cursor']
    connection = current_app.config['connection']
    account = getAccount()

    if request.method == 'GET':
        return get_one_public_schedule(account, cursor, scheduleID)