import { useContext, useState } from "react"
import { CLogin } from "../../classes/login";
import { useNavigate } from 'react-router-dom';
import { AuthContext } from "../../contexts/auth";

export default function LoginPage({target = "/"}) {
    const navigate = useNavigate();

    const context = useContext(AuthContext);

    const [login, setLogin] = useState<CLogin>(new CLogin());
    const [pending, setPending] = useState(false);

    const handleFieldChange = (e: React.FormEvent<HTMLInputElement | HTMLTextAreaElement>): void => {
        setLogin({
            ...login,
            [e.currentTarget.id]: e.currentTarget.value,
        });
    };

    const handleSubmit = async (e:React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if(pending) {
            return;
        }

        setPending(true);

        const currentUser = await context.login(login);

        if(currentUser.isAuthenticated) {
            navigate(target);             
        } else {
            alert('Login Failed!');
        }
        
        setPending(false);   
    }

    return (
    <>
    <form onSubmit={handleSubmit}>
        <input id="username" value={login.username} onChange={handleFieldChange} />
        <input id="password" type="password" value={login.password}  onChange={handleFieldChange}/>
        <button type="submit" disabled={pending}>Login</button>
    </form>
    </>
    )
}