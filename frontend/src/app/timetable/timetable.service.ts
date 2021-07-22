import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Dests, Time } from '../timetable/dests';
import { map } from 'rxjs/operators';


@Injectable({
  providedIn: 'root'
})
export class TimetableService {
  private destsUrl = 'http://localhost:8000/destinations/';
  
  constructor(private http: HttpClient) { 
    this.http = http;
  }

  getDestinations(): Observable <Dests[]>{
    return this.http.get<Dests[]>(this.destsUrl);
}
   // return this.http.get<Dests[]>(baseUrl);
   getByZone(id: any): Observable<Dests[]> {
    return this.http.get<Dests[]>(`${this.destsUrl}${id}`);
}
  getDetails(id: any): Observable<Time[]> {
    return this.http.get<Time[]>(`http://localhost:8000/timetable/${id}`).pipe(map(res => res));
}
}
