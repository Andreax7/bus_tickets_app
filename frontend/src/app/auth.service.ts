import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';
import {BehaviorSubject , Observable, throwError} from 'rxjs';
import { Router } from '@angular/router';
import { User } from './register/user';
import { CookieService } from 'ngx-cookie';



@Injectable({
  providedIn: 'root'
})

export class AuthService {


  private httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };
  
  csrf!: string;

  public token!: any;

  public username?:string;

  public errors: any = [];

  public token_expires!: Date;
  private  headers = new HttpHeaders({'Content-Type': 'application/json',
                              'Access-Control-Allow-Origin': '*',
                             // 'X-CSRFToken': this.cookieService.get("csrftoken"),
                              'Authorization':'JWT '+ localStorage.getItem("user")});
  constructor(private http: HttpClient, public router: Router, private cookieService: CookieService) {
    
    let csrf = this.cookieService.get("csrftoken");// get csrf token from the cookie
    if (typeof(csrf) === 'undefined') { 
      csrf = '';
    }
    this.httpOptions = {
      headers: new HttpHeaders({
                  'Accept': 'application/json',
                  'Access-Control-Allow-Origin': '*',
       //           'X-CSRFToken': csrf,//add value of csrf into the HttpHeaders  
      }) 
    };
  }

  checkUsername(username:string): Observable<any> {
   return this.http.get('http://localhost:8000/checkuser/' + username);
  }

  checkEmail(email:string): Observable<any> {
    return this.http.get('http://localhost:8000/checkmail/' + email);
   }

  register(user: User): Observable<User> {
    return this.http.post<User>('http://localhost:8000/' + 'register/', user, this.httpOptions);
  }

  login(username:string, password:string){
    return this.http.post<User>('http://localhost:8000/auth/',{username,password}, this.httpOptions).subscribe(
      data => {
        localStorage.setItem("user",data['token']);
        this.token = data['token'];
        console.log(this.token);
      },
      err => {
        this.errors = err.error;
      }
     
    );
  };
  
  myprofiledata(){
    return this.http.post('http://localhost:8000/myprofile/', {headers:this.headers,withCredentials:true});
  }

  getAuthToken(username:string, password:string) {
    return this.http.post<User>('http://localhost:8000/auth/', {username,password}, this.httpOptions).pipe(
      map(res => {
        if (res){
          localStorage.setItem("user",res["token"]);
          console.log(res["token"]);

        }
      }),
    );
  }


  logout() {
    localStorage.removeItem("user");
    localStorage.removeItem("expires_at");
}

}

