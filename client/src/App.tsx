import LoginPage from './pages/auth/LoginPage';
import LogoutPage from './pages/auth/LogoutPage';
import RegisterPage from './pages/auth/RegisterPage';
import HomePage from './pages/home';
import LayoutPage from './pages/layout';
import './styles/App.css'

import {
    createBrowserRouter,
    RouterProvider,
} from "react-router-dom";

const router = createBrowserRouter([
    {
        path: "/",
        element: <LayoutPage />, 
        // errorElement: <ErrorPage />,
        children: [
            {
                path: "/",
                element: <HomePage />,
            },
            {
                path: "/login",
                element: <LoginPage />,
            },
            {
                path: "/register",
                element: <RegisterPage />,
            },
            {
                path: "/logout",
                element: <LogoutPage />,
            },
        ]
    },

]);



function App() {

    return (
        <RouterProvider router={router} />
    )
}

export default App
