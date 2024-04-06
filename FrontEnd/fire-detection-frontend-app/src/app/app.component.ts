import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { FireListComponent } from './fire-list/fire-list.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet,FireListComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'fire-detection-frontend-app';
}
