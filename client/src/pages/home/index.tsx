import { useContext } from "react";
import { AuthContext } from "../../contexts/auth";

export default function HomePage() {
    const context = useContext(AuthContext);
    return (
        <>
            <h1>Welcome Home {context.user.name}</h1>

        </>
    )
}