
import { invalid } from '@angular/compiler/src/render3/view/util';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators, FormGroup, FormControl } from '@angular/forms';
import { AuthService } from '../auth.service';


@Component({
  selector: 'app-nav',
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.css']
})

export class NavComponent implements OnInit {
  
  loginForm: FormGroup;
  showModal = false;
  submitted = false;
  public unexists!: string;

  constructor( private formBuilder: FormBuilder,
              public authService: AuthService) { 
      
          this.loginForm = this.formBuilder.group({
          username: ['',  [Validators.required]],
          password: ['', [Validators.required]]
                });
  }

 ngOnInit() { 
  }

  show(){
    this.showModal = true;
  }
  hide(){
    this.showModal = false;
  }

 

  UsernameUnique() {
    var username = this.loginForm.controls['username'].value;
    this.authService.checkUsername(username)
    .subscribe(
      response => {
        if( response == 'true' ){
          this.unexists = ' ';
        };
        if( response === 'false' ){ 
          this.unexists = 'User does not exist';
          this.loginForm.controls.username.setErrors({'invalid': true});
        }
      }
    );
  }
  
  submit() {
    const username = this.loginForm.controls['username'].value;
    const password = this.loginForm.controls['password'].value;
    if(this.loginForm.valid)
      {
        this.authService.login(username, password)//.subscribe(
   //       response => {
     //       console.log(response)
    //      });    
        
      }
   }
  
}