from flask import Flask, jsonify, request
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from flask_redis import FlaskRedis
import json

from dateutil import parser
from datetime import datetime, timedelta, timezone, time
from dateutil.relativedelta import relativedelta
app = Flask(__name__)
app.debug = True
app.config['MONGODB_SETTINGS'] = {
    'db': 'mydatabase',
    'host': 'mongodb://mongodb:27017/mydatabase'
}
app.config['REDIS_URL'] = 'redis://redis:6379/0'

CORS(app)

db = MongoEngine(app)
redis_store = FlaskRedis(app)

class User(db.Document):
    name = db.StringField(required=True)
    age = db.IntField(required=True)

class Showtime(db.Document):
    name = db.StringField(required=True)
    length = db.StringField(required=True)
    time = db.StringField(required=True)  # 使用 ISO 8601 字符串格式
    entrance = db.StringField(required=True)

def init_movies_data():
    if Showtime.objects.count() == 0:  # 檢查數據庫是否已經有數據
        movies_data = [
            {"name": "Aqua man 2", "length": "2 hours", "time": "2023-12-20T12:30:00.00+08:00", "entrance": "2F-A"},
            {"name": "Wish", "length": "1 hours 50 minutes", "time": "2023-12-29T17:30:00.00+08:00", "entrance": "2F-B"},
            {"name": "Unicorn Galaxy", "length": "1 hour 55 minutes", "time": "2023-11-15T14:00:00.00+08:00", "entrance": "1F-C"},
            {"name": "Unicorn Galaxy", "length": "1 hour 55 minutes", "time": "2023-12-01T16:30:00.00+08:00", "entrance": "1F-C"},
            {"name": "Unicorn Galaxy", "length": "1 hour 55 minutes", "time": "2024-01-02T18:00:00.00+08:00", "entrance": "1F-C"},
            {"name": "Batman Returns", "length": "2 hours 30 minutes", "time": "2023-12-21T14:30:00.00+08:00", "entrance": "1F-C"},
            # Add more movies if needed
        ]
        for movie in movies_data:
            new_showtime = Showtime(**movie)
            new_showtime.save()
        print("Movie showtimes initialized.")
    else:
        print("Database already initialized.")

@app.route('/api/users', methods=['GET'])
def get_users():
    # Check Redis cache first
    users_data = redis_store.get('users')
    # app.logger.info(      users_data)
    if users_data:
        users = users_data.decode('utf-8')  # Convert binary to string
    else:
        users = User.objects().to_json()
        # app.logger.info(users)
        # Store data in Redis cache
        redis_store.set('users', users)
    return users, 200

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.objects.get_or_404(id=user_id)
    return jsonify(user), 200

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(name=data['name'], age=data['age'])
    user.save()
    # Clear Redis cache
    redis_store.delete('users')
    return jsonify(user), 201


@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.objects.get_or_404(id=user_id)
    user.name = data['name']
    user.age = data['age']
    user.save()
    # Clear Redis cache
    redis_store.delete('users')
    return jsonify(user), 200

@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.objects.get_or_404(id=user_id)
    user.delete()
    # Clear Redis cache
    redis_store.delete('users')
    return jsonify({'message': 'User deleted'}), 200
@app.route('/api/movies/weekly-schedule', methods=['GET'])
def weekly_schedule():
    start_time = time(11, 0)  # Set start time filter
    end_time = time(23, 0)    # Set end time filter

    # Query the database for all showtimes within the specified time range
    week_schedule = {}
    for showtime in Showtime.objects:
        try:
            # Parse the datetime first
            show_dt = parser.parse(showtime.time)
            # Apply timezone correction only if tzinfo is None
            show_dt = show_dt if show_dt.tzinfo else show_dt.replace(tzinfo=timezone.utc)

            if start_time <= show_dt.time() <= end_time:
                day = show_dt.strftime('%A')
                if day not in week_schedule:
                    week_schedule[day] = []
                week_schedule[day].append({
                    "Name": showtime.name,
                    "Time": showtime.time,
                    "Entrance": showtime.entrance
                })
        except ValueError as e:
            print(f"Error parsing datetime for showtime {showtime.time}: {e}")

    return jsonify(week_schedule)

@app.route('/api/movies/monthly-schedule', methods=['GET'])
def monthly_schedule():
    movie_name = request.args.get('name')
    month = request.args.get('month')  # Expected format 'YYYY-MM'

    if not movie_name or not month:
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        month_start = datetime.strptime(month, '%Y-%m').replace(tzinfo=timezone.utc)
        month_end = month_start + relativedelta(months=1)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    month_schedule = []
    for showtime in Showtime.objects(name=movie_name):
        try:
            show_dt = parser.parse(showtime.time)
            # Apply timezone correction only if tzinfo is None
            show_dt = show_dt if show_dt.tzinfo else show_dt.replace(tzinfo=timezone.utc)

            if month_start <= show_dt < month_end:
                month_schedule.append({
                    "Name": showtime.name,
                    "Date": show_dt.strftime('%Y-%m-%d'),
                    "Time": show_dt.strftime('%H:%M'),
                    "Entrance": showtime.entrance
                })
        except ValueError as e:
            print(f"Error parsing datetime for showtime {showtime.time}: {e}")

    return jsonify(month_schedule)
    
if __name__ == '__main__':
    init_movies_data()
    app.run(host='0.0.0.0', port=5000)