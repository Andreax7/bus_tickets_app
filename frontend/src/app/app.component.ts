import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'StBus_app';

  ngOnInit() {
  const token = localStorage.getItem("token");
//  const user = JSON.parse(localStorage.getItem("user"));
}
}