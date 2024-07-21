from flask import Flask, request, jsonify
from flask_cors import CORS
from models import  Event
from Services import EventService
from tasks import process_event
from datetime import datetime
from redis import Redis
from rq import Queue

app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "*"}})  # Restrict origins as needed
CORS(app)

# Redis Queue
redis_conn = Redis(host='localhost', port=6379)
queue = Queue(connection=redis_conn)

event_service = EventService()

@app.route('/')
def display():
    return "Hello, welcome to the Python server"

@app.route('/api/events', methods=['POST'])
def receive_event():
    data = request.get_json()
    timestamp = datetime.strptime(data['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")
    event_data = {
        'device_id': data['device_id'],
        'timestamp': timestamp,
        'event_type': data['event_type'],
        'event_data': data['event_data']
    }
    job = queue.enqueue(process_event, event_data)
    return jsonify({"message": "Event stored successfully", "job_id": job.get_id()}), 200


@app.route('/api/events/query', methods=['GET'])
def query_events():
    device_id = request.args.get('device_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Ensure proper datetime conversion
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ")

    events = event_service.query_events(device_id, start_date, end_date)
    return jsonify([event.to_dict() for event in events])

@app.route('/api/events/summary', methods=['GET'])
def summary_report():
    device_id = request.args.get('device_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Ensure proper datetime conversion
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ")

    summary = event_service.summary_report(device_id, start_date, end_date)
    return jsonify(summary)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

