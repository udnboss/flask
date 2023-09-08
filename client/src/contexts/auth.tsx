import { ReactNode, createContext, useReducer } from "react";
import { CLogin } from "../classes/login";
import AuthApi from "../services/api/auth";

export class CurrentUser {
    username: string = "guest";
    name: string = "Guest";
    email?: string;
    isAuthenticated: boolean = false;    
}

type AuthContextType = {
    user: CurrentUser;
    login: (login:CLogin) => Promise<CurrentUser>;
    logout: () => Promise<CurrentUser>;
}

export const AuthContext = createContext<AuthContextType>({user: new CurrentUser()} as AuthContextType);

type authReducerAction = {
    type: string;
    user: CurrentUser;
}

function authReducer(user: CurrentUser, action: authReducerAction): CurrentUser {
    console.log(`received: ${action.type} on ${action.user.name}`)
    switch(action.type) {
        case 'loggedin': {
            return action.user;
        }
        case 'loggedout': {
            return action.user;
        }
        default: {
            return user;
            throw Error('Unknown action: ' + action.type);
        }
    }
}

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, dispatch] = useReducer(authReducer, new CurrentUser());
    const authApi = new AuthApi();

    const login = async (login:CLogin) => {
        
        try {
            const currentUser = await authApi.login(login);
            dispatch({type: 'loggedin', user: currentUser});
            return currentUser;
        } catch (error) {
            alert(error);
            return new CurrentUser();
        }
    };

    const logout = async () => {
        try {
            await authApi.logout();
            const currentUser = new CurrentUser();
            dispatch({type: 'loggedout', user: currentUser});
            return currentUser;
        } catch (error) {
            alert(error);
            return new CurrentUser();
        }
    };

    const value = { user, login, logout };
   
    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    )
}