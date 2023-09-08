import { CLogin } from "../../classes/login";
import { CurrentUser } from "../../contexts/auth";

export default class AuthApi {
    constructor() {

    }

    async login(login:CLogin):Promise<CurrentUser> {
        return new Promise((resolve, reject) => {
            if(login.username == 'ali') {
                const user = new CurrentUser();
                user.username = login.username;
                user.isAuthenticated = true;
                user.name = "Ali";
                user.email = "ali@example.com";
                resolve(user);
            } else {
                reject(new Error("Login failed")); 
            }                  
        });
    }

    async register(login:CLogin):Promise<boolean> {
        return new Promise((resolve, reject) => {

            if(login.username != null && login.password != null)
                resolve(true);
            else 
                reject(false);   
        });
    }

    async logout():Promise<boolean> {
        return new Promise((resolve) => {
            resolve(true);
        });    
    }
}