import { Component, OnInit } from '@angular/core';
import { Dests, Time } from '../timetable/dests';
import { TimetableService } from './timetable.service';


@Component({
  selector: 'app-timetable',
  templateUrl: './timetable.component.html',
  styleUrls: ['./timetable.component.css']
})  



export class TimetableComponent implements OnInit {
  dests?: Dests[];
  times?: Time[];
  showTimetable = false;

  
  constructor(private TimetableService: TimetableService) {
  }
    
  ngOnInit(): void {
    this.allDest();
    
  }

  allDest() {
    this.TimetableService.getDestinations().subscribe(
      res => {
        this.dests=res;
          console.log(this.dests);
      },
      error =>{
        console.log(error);
      }
    );
  }

  getByZone(zoneid: string) {
    this.TimetableService.getByZone(zoneid).subscribe(res => {
        this.dests = res;
    });
}

getDetail(id: number) {
  this.showTimetable = true;
  this.TimetableService.getDetails(id).subscribe(res => {
      this.times = res;
  });
}

}
