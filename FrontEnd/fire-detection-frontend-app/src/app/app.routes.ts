import { Routes } from '@angular/router';
import { VideoPlayerComponent } from './video-player/video-player.component';

export const routes: Routes = [
    { path: 'video/:id', component: VideoPlayerComponent }
];
