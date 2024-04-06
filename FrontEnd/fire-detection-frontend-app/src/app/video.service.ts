import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class VideoService {
  play(videoUrl: string) {
    window.open(videoUrl,`_blank`)
  }

  constructor() { }
}
