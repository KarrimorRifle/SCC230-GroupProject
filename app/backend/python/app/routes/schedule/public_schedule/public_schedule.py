from flask import request, jsonify, Blueprint, current_app
from ...accounts import getAccount
from iota import genRandomID

public_schedule = Blueprint('public_schedule', __name__)



@public_schedule.route('/schedule/public', methods=['GET'])
def get_public_schedules():
    cursor = current_app.config['cursor']

    cursor.execute("SELECT ScheduleID, ScheduleName, IsActive, IsPublic, Rating, IsDraft FROM schedules WHERE IsPublic = 1")
    schedules = [schedule for schedule in cursor.fetchall()]
    schedules = sorted(schedules, key=lambda x: (-x['Rating'], x['ScheduleName']), reverse=True)
    return jsonify(schedules), 200