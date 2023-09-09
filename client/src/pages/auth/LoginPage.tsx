import { useState } from "react"
import { CLogin } from "../../classes/login";
import { useNavigate } from 'react-router-dom';
import { useAuthContext } from "../../contexts/AuthContext";

export default function LoginPage({target = "/"}) {
    const navigate = useNavigate();

    const authContext = useAuthContext();

    const [login, setLogin] = useState<CLogin>(new CLogin());

    const handleFieldChange = (e: React.FormEvent<HTMLInputElement | HTMLTextAreaElement>): void => {
        setLogin({
            ...login,
            [e.currentTarget.id]: e.currentTarget.value,
        });
    }

    const handleSubmit = async (e:React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if(authContext.user.isPending) {
            return;
        }

        const currentUser = await authContext.login(login);

        if(currentUser.isAuthenticated) {
            navigate(target);             
        } else {
            alert('Login Failed!');
        }
    }

    return (
    <>
    <form onSubmit={handleSubmit}>
        <input id="username" value={login.username} onChange={handleFieldChange} />
        <input id="password" type="password" value={login.password} onChange={handleFieldChange}/>
        <button type="submit" disabled={authContext.user.isPending}>Login</button>
    </form>
    </>
    )
}