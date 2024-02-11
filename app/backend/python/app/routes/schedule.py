from flask import request, jsonify, make_response, Blueprint, current_app
from accounts import getAccount

schedule = Blueprint('schedule', __name__)


def get_schedules(account, cursor, connection):
    query = ("SELECT EventID, ScheduleName, IsActive, IsPublic, Rating FROM schedules "
                "WHERE AuthorID = %s")
    
    cursor.execute(query, (account['AccountID'],))
    schedules = cursor.fetchall()
    return jsonify(schedules)

#TO BE UPDATED BASED ON TRIGGER AND HUB
def create_schedule(account, cursor, connection):
    query = ("INSERT INTO schedule (ScheduleName, AuthorID, HubID, TriggerID, IsActive, IsPublic, Rating) "
                     "VALUES ('{}','{}','{}','{}','{}','{}','{}')".format(request.json.get("ScheduleName"),account['AccountID'],None, None, request.json.get("IsActive"), request.json.get("IsPublic"), request.json.get("Rating")))
    try:
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 500
    
    query = ("INSERT INTO ")
    
    return jsonify({'success':'Schedule Created'})

@schedule.route("/accounts" , methods=['POST', 'PATCH', 'DELETE', 'GET'])
def scheduleResponse(self):
    account = getAccount()
    if account is None:
        return jsonify({"error": "Session ID is invalid"}), 401
    cursor = current_app.config['cursor']
    connection = current_app.config['connection']

    if request.method == 'GET':
        return get_schedules(account, cursor, connection)

    cursor.close()
    connection.close()