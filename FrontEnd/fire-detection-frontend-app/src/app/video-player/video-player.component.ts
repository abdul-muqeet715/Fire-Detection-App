import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-video-player',
  templateUrl: './video-player.component.html',
  styleUrls: ['./video-player.component.css']
})
export class VideoPlayerComponent  {

  @Input() videoUrl !: string;

  constructor(private router: Router) {}

  close() {
    // Logic to close the modal
    this.router.navigate(['/']); // Redirect to home page
  }

}
