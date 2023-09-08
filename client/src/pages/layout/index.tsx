import { Outlet } from "react-router-dom";
import { AuthProvider } from "../../contexts/auth";

export default function LayoutPage() {    
    return (
        <AuthProvider>
            <h1>Welcome Layout</h1>
            <Outlet />    
        </AuthProvider>
    )
}