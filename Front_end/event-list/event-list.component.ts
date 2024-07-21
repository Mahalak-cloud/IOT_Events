import { Component } from '@angular/core';
import { EventService } from '../event.service';

@Component({
  selector: 'app-event-list',
  templateUrl: './event-list.component.html',
  styleUrl: './event-list.component.css'
})
export class EventListComponent {
  device_id: string = '';
  start_date: string = '';
  end_date: string = '';
  events: any[] = [];

  constructor(private eventService: EventService) { }

  async getEvents() {
    try {
      const response = await this.eventService.getEvents(this.device_id, this.start_date, this.end_date);
      console.log(response);
      console.log(response.data);
      console.log(this.start_date);
      console.log(this.end_date);
      this.events = response.data;
      console.log(this.events);
    } catch (error) {
      console.error(error);
    }
  }
  async addEvent() {
    console.log('method addEvent Start');
    const event = {
      device_id: this.device_id,
      timestamp: new Date().toISOString(),
      event_type: 'temperature',
      event_data: Math.random() * 100
    };
    console.log(event);
    try {
      await this.eventService.addEvent(event);
      alert('Event added successfully');
      // this.getEvents();
    } catch (error) {
      console.error(error);
    }
  }
}
