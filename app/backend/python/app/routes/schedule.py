from flask import request, jsonify, make_response, Blueprint, current_app
from accounts import getAccount

schedule = Blueprint('schedule', __name__)


def get_schedules(account, cursor):
    query = ("SELECT EventID, ScheduleName, IsActive, IsPublic, Rating FROM schedules "
                "WHERE AuthorID = %s")
    
    cursor.execute(query, (account['AccountID'],))
    schedules = cursor.fetchall()
    return jsonify(schedules), 200

#TO BE UPDATED BASED ON DATABASE ID CHANGES
def create_schedule(account, cursor, connection):
    # ADD SCHEDULE ID CHANGES TO ENTER INTO DB BASED ON FUTURE CHANGES
    scheduleName = request.json.get("ScheduleName")
    query = ("INSERT INTO schedule (ScheduleName, AuthorID, IsActive, IsPublic, Rating) "
                     "VALUES ('{}','{}','{}','{}','{}')".format(scheduleName, account['AccountID'], request.json.get("IsActive"), request.json.get("IsPublic"), None))
    try:
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 500
    
    # UPDATE THIS SECTION BASED ON ID CHANGES IN DB
    query = ("SELECT EventID FROM schedules "
                "WHERE ScheduleName = %s AND AuthorID = %s")
    
    cursor.execute(query, (scheduleName, account['AccountID'],))

    scheduleID = cursor.fetchone()

    if scheduleID is None:
        return jsonify({"error":"Schedule ID could not be retrieved"}), 500

    return jsonify(scheduleID), 200

def delete_schedule(account, cursor, connection):
    query = ("DELETE FROM schedules WHERE AuthorID = %s AND EventID = %s" )

@schedule.route("/schedule" , methods=['POST', 'GET'])
def scheduleResponse(self):
    account = getAccount()
    if account is None:
        return jsonify({"error": "Session ID is invalid"}), 401
    cursor = current_app.config['cursor']
    connection = current_app.config['connection']

    if request.method == 'GET':
        return get_schedules(account, cursor)
    elif request.method == 'POST':
        return create_schedule(account, cursor, connection)

    cursor.close()
    connection.close()