from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory database to store bookings (can replace with actual database in real use case)
bookings = []

# Helper function to check if there is a conflict with existing bookings
def check_conflict(room, start_time, end_time):
    for booking in bookings:
        if booking['room'] == room:
            # Check if the requested timeslot overlaps with an existing booking
            if (start_time < booking['end_time'] and end_time > booking['start_time']):
                return True
    return False

@app.route('/book', methods=['POST'])
def book_room():
    data = request.get_json()

    # Validate input
    try:
        room = data['room']
        start_time = datetime.strptime(data['start_time'], '%Y-%m-%dT%H:%M:%S')
        end_time = datetime.strptime(data['end_time'], '%Y-%m-%dT%H:%M:%S')
    except KeyError or ValueError:
        return jsonify({"error": "Invalid input data"}), 400

    # Check for conflicts
    if check_conflict(room, start_time, end_time):
        return jsonify({"error": "Room is already booked for the requested time."}), 409

    # Add booking to "database"
    bookings.append({
        'room': room,
        'start_time': start_time,
        'end_time': end_time
    })

    return jsonify({"message": "Room booked successfully!"}), 200

@app.route('/bookings', methods=['GET'])
def get_bookings():
    # Return all current bookings
    return jsonify([{
        'room': booking['room'],
        'start_time': booking['start_time'].strftime('%Y-%m-%dT%H:%M:%S'),
        'end_time': booking['end_time'].strftime('%Y-%m-%dT%H:%M:%S')
    } for booking in bookings])

if __name__ == '__main__':
    app.run(debug=True)
