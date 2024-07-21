from sqlalchemy import func
from models import Event, Session

class EventService:
    def __init__(self):
        self.session = Session()

    def add_event(self, event):
        self.session.add(event)
        self.session.commit()

    def query_events(self, device_id, start_date, end_date):
        query = self.session.query(Event).filter(Event.device_id == device_id)

        if start_date and end_date:
            query = query.filter(Event.timestamp.between(start_date, end_date))

        return query.all()

    def summary_report(self, device_id, start_date, end_date):
        query = self.session.query(Event).filter(Event.device_id == device_id)

        if start_date and end_date:
            query = query.filter(Event.timestamp.between(start_date, end_date))

        max_temp = query.with_entities(func.max(Event.event_data)).scalar()
        min_temp = query.with_entities(func.min(Event.event_data)).scalar()
        avg_temp = query.with_entities(func.avg(Event.event_data)).scalar()

        return {"max_temp": max_temp, "min_temp": min_temp, "avg_temp": avg_temp}
