import { Component } from '@angular/core';
import { EventService } from '../event.service';

@Component({
  selector: 'app-event-summary',
  templateUrl: './event-summary.component.html',
  styleUrl: './event-summary.component.css'
})
export class EventSummaryComponent {
  device_id: string = '';
  start_date: string = '';
  end_date: string = '';
  summary: any = null;

  constructor(private eventService: EventService) { }

  async getSummary() {
    try {
      const response = await this.eventService.getSummary(this.device_id, this.start_date, this.end_date);
      this.summary = response.data;
    } catch (error) {
      console.error(error);
    }
  }
}
