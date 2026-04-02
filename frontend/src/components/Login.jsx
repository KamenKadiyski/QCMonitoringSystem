import { useState } from 'react';
import axios from 'axios'; // Тук ползваме чист axios, защото още нямаме токен

const Login = () => {
    const [credentials, setCredentials] = useState({ username: '', password: '' });
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            // Пътят трябва да съвпада с TokenObtainPairView в Django urls.py
            const res = await axios.post('http://127.0.0.1', credentials);

            // Записваме токените, които api.js ще използва автоматично
            localStorage.setItem('access', res.data.access);
            localStorage.setItem('refresh', res.data.refresh);

            alert("Влязохте успешно!");
            window.location.href = '/'; // Пренасочване към началната страница
        } catch (err) {
            setError("Грешно потребителско име или парола");
        }
    };

    return (
        <div style={{ maxWidth: '300px', margin: '100px auto', padding: '20px', border: '1px solid #ccc' }}>
            <h3>Login</h3>
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                <input
                    placeholder="Username"
                    onChange={e => setCredentials({...credentials, username: e.target.value})}
                />
                <input
                    type="password"
                    placeholder="Password"
                    onChange={e => setCredentials({...credentials, password: e.target.value})}
                />
                <button type="submit" style={{ backgroundColor: '#28a745', color: 'white', border: 'none', padding: '10px' }}>
                    Login
                </button>
            </form>
            {error && <p style={{ color: 'red', fontSize: '12px' }}>{error}</p>}
        </div>
    );
};

export default Login;
