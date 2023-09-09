import { ReactNode, useReducer } from "react";
import { CLogin } from "../classes/login";
import AuthApi from "../services/api/auth";
import { AuthContext, AuthContextReducer, CurrentUser } from "./AuthContext";

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, dispatch] = useReducer(AuthContextReducer, new CurrentUser());

    const authApi = new AuthApi();

    const login = async (login:CLogin) => {
        
        try {
            dispatch({type: 'pending', user: user});
            const currentUser = await authApi.login(login);
            dispatch({type: 'loggedin', user: currentUser});
            return currentUser;
        } catch (error) {
            dispatch({type: 'loginfailed', user: user});
            alert(error);
            return user;
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