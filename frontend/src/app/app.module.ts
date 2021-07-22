import { NgModule } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { CookieModule } from 'ngx-cookie';

import { AppRoutingModule } from './app-routing.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { NavComponent } from './nav/nav.component';
import { TimetableComponent } from './timetable/timetable.component';

import { FormsModule, ReactiveFormsModule } from '@angular/forms';


import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
import { FlexLayoutModule } from '@angular/flex-layout';



import { AuthService } from './auth.service';
import { TimetableService } from './timetable/timetable.service';
import { RegisterComponent } from './register/register.component';
import { AboutComponent } from './about/about.component';
import { GetTicketComponent } from './get-ticket/get-ticket.component';
import { UserPanelComponent } from './user-panel/user-panel.component';
import { AdminPanelComponent } from './admin-panel/admin-panel.component';
import { AuthInterceptor } from './auth.interceptor';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    TimetableComponent,
    NavComponent,
    RegisterComponent,
    AboutComponent,
    GetTicketComponent,
    UserPanelComponent,
    AdminPanelComponent
  ],
  imports: [
    BrowserModule,
    CookieModule.forRoot() ,
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule,
    FormsModule,

    ReactiveFormsModule,
    MatToolbarModule,
    MatIconModule,
    MatButtonModule,
    MatTableModule,
    FlexLayoutModule, 
    NgbModule,
  
  ],
  providers: [ AuthService, TimetableService, AuthInterceptor ],
  bootstrap: [AppComponent]
})
export class AppModule { }
