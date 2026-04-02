import { useEffect, useState } from 'react';
import api, { logout } from '../api.js';

const Sidebar = () => {
    const [menuItems, setMenuItems] = useState([]);

    useEffect(() => {
        // КОРИГИРАН ПЪТ: Добавяме префикса, който ползваме и в другите компоненти
        api.get('accounts/api/menu-items/')
            .then(res => setMenuItems(res.data))
            .catch(err => {
                console.log("Грешка при зареждане на менюто (404 или липса на права)", err);
            });
    }, []);

    return (
        <nav className="sidebar" style={{ width: '250px', padding: '15px', background: '#f8f9fa', borderRight: '1px solid #ccc' }}>
            <h3 style={{ fontSize: '18px', marginBottom: '20px' }}>Menu</h3>
            <div className="menu-list">
                {menuItems.map((item, index) => (
                    <div key={index} className="menu-item" style={{ marginBottom: '15px', cursor: 'pointer' }}>
                        {item.icon && <i className={`bi bi-${item.icon}`} style={{ marginRight: '10px' }}></i>}
                        <span>{item.title}</span>
                    </div>
                ))}
            </div>

            <hr style={{ margin: '20px 0' }} />

            <button
                onClick={logout}
                style={{
                    width: '100%',
                    padding: '10px',
                    color: 'white',
                    backgroundColor: '#dc3545',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    fontWeight: 'bold'
                }}
            >
                Logout
            </button>
        </nav>
    );
};

export default Sidebar;
