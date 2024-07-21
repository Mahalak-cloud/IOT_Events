from models import Event, Session
from datetime import datetime

def process_event(data):
    session = Session()
    timestamp = datetime.strptime(data['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")
    event = Event(
        device_id=data['device_id'],
        timestamp=timestamp,
        event_type=data['event_type'],
        event_data=data['event_data']
    )

    session.add(event)
    session.commit()
    session.close()
