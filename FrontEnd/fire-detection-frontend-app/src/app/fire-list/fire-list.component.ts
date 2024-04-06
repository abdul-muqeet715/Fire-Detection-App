import { Component, OnInit } from '@angular/core';
import { Fire } from '../fire.model';
import { FireService } from '../fire.service';
import { MapService } from '../map.service';
import { VideoPlayerComponent } from '../video-player/video-player.component';
import { NgFor, NgIf } from '@angular/common';
import { RouterLink } from '@angular/router';
import { VideoService } from '../video.service';

@Component({
  standalone: true,
  selector: 'app-fire-list',
  templateUrl: './fire-list.component.html',
  styleUrls: ['./fire-list.component.css'],
  imports: [NgFor, RouterLink,NgIf,VideoPlayerComponent]
})
export class FireListComponent implements OnInit {

  fireIncidents: Fire[] = [];
  isModalOpen : boolean = false;

  constructor(private fireService: FireService, 
    private mapService: MapService,
  private videoService: VideoService) { }

  ngOnInit(): void {
    this.loadFireIncidents();
  }

  loadFireIncidents(): void {
    this.fireService.getAllFireIncidents().subscribe(data => {
      this.fireIncidents = data;
    });
  }

  openVideo(videoUrl:string) {
    this.videoService.play(videoUrl);
  }

  openMap(latitude: string, longitude: string) {
    latitude = ''
    this.mapService.openMap(latitude, longitude);
  }
}
