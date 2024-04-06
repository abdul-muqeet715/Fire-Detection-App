import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class MapService {

  constructor() { }

  openMap(latitude: string, longitude: string) {
    window.open(`https://www.google.com/maps?q=${17.385044},${78.460770}`);
  }
}
