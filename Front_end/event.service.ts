import { Injectable } from '@angular/core';
import axios from 'axios';

@Injectable({
  providedIn: 'root'
})
export class EventService {
  private baseUrl = 'http://127.0.0.1:5000/api/events';

  constructor() { }

  async addEvent(event: any) {
    console.log('addEvent Service method');
    try {
      return await axios.post(this.baseUrl, event);
    } catch (error) {
      console.error('Error adding event:', error);
      throw error;  // rethrow for caller to handle
    }
  }

  async getEvents(device_id: string, start_date: string, end_date: string) {
    const url = `${this.baseUrl}/query?device_id=${device_id}&start_date=${start_date}&end_date=${end_date}`;
    return axios.get(url);
  }

  async getSummary(device_id: string, start_date: string, end_date: string) {
    const url = `${this.baseUrl}/summary?device_id=${device_id}&start_date=${start_date}&end_date=${end_date}`;
    return axios.get(url);
  }
}
