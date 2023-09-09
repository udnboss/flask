import { createContext, useContext } from "react";
import { CLogin } from "../classes/login";

export class CurrentUser {
    username: string = "guest";
    name: string = "Guest";
    email?: string;
    isPending: boolean = false;
    isAuthenticated: boolean = false;    
}

type AuthContextType = {
    user: CurrentUser;
    // pending: boolean;
    login: (login:CLogin) => Promise<CurrentUser>;
    logout: () => Promise<CurrentUser>;
}

export const AuthContext = createContext<AuthContextType>({user: new CurrentUser()} as AuthContextType);

type authReducerAction = {
    type: string;
    user: CurrentUser;
}

export function AuthContextReducer(user: CurrentUser, action: authReducerAction): CurrentUser {
    console.log(`received: ${action.type} on ${action.user.name}`)
    switch(action.type) {
        case 'pending': {
            action.user.isPending = true;
            return action.user;
        }
        case 'loggedin': {
            action.user.isPending = false;
            return action.user;
        }
        case 'loginfailed': {
            user.isPending = false;
            return user;
        }
        case 'loggedout': {
            action.user.isPending = false;
            return action.user;
        }
        default: {
            user.isPending = false;
            return user;
            throw Error('Unknown action: ' + action.type);
        }
    }
}

export function useAuthContext() {
    const context = useContext(AuthContext);

    if (context === undefined) {
        throw new Error("useAuthContext was used outside of its Provider");
    }

    return context;
}