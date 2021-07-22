

export class User {
    id?: number;
    username?: string;
    password?: string;
    first_name?: string;
    last_name?: string;
    address?: string;
    role?: string; 
    token!: string;
    picture?: string;
}

export class Employees{
    id?:number;
    username?: string;
    password?: string;
    is_active?: string;
    is_staff?: string;
    first_name?: string;
    last_name?: string;
    address?: string;
    token!: string;
}
