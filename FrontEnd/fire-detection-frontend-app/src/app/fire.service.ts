import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Fire } from './fire.model';

@Injectable({
  providedIn: 'root'
})
export class FireService {

  private apiUrl = 'http://localhost:8080/'; // Replace this with your API endpoint URL

  constructor(private http: HttpClient) { }

  getAllFireIncidents(): Observable<Fire[]> {
    return this.http.get<Fire[]>(this.apiUrl);
  }
  getVideoUrlById(id:number): Observable<String>{
    const url = `${this.apiUrl}/urls/${id}`; // Assuming your backend API endpoint to fetch URL by ID is '/urls/:id'
    return this.http.get<string>(url);
  }
}
