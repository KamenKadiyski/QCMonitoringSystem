import { useState, useEffect } from 'react';
import api from '../api.js';

const EmployeeList = () => {
    const [employees, setEmployees] = useState([]);

    const fetchEmployees = () => {
        // Използваме пътя от Django API
        api.get('accounts/api/employees/')
            .then(res => {
                setEmployees(res.data || []);
            })
            .catch(err => {
                console.error("Грешка при зареждане:", err);
                if (err.response?.status === 403 || err.response?.status === 401) {
                    console.log("Сесията е невалидна или изтекла");
                }
            });
    };

    useEffect(() => {
        fetchEmployees();
    }, []);

    const handleDelete = async (id) => {
        if (window.confirm("Сигурни ли сте, че искате да изтриете този служител?")) {
            try {
                // CSRF се добавя автоматично от api.js
                await api.delete(`accounts/api/employees/${id}/`);
                fetchEmployees();
            } catch (err) {
                alert("Грешка при изтриване!");
            }
        }
    };

    const handleUpdateName = async (id, currentName) => {
        const newName = prompt("Въведете ново име:", currentName);
        if (newName && newName !== currentName) {
            try {
                await api.patch(`accounts/api/employees/${id}/`, { first_name: newName });
                fetchEmployees();
            } catch (err) {
                alert("Грешка при обновяване!");
            }
        }
    };

    return (
        <div style={{ marginTop: '20px' }}>
            <h3>Списък със служители</h3>
            <table border="1" style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse', fontSize: '14px' }}>
                <thead>
                <tr style={{ backgroundColor: '#f2f2f2' }}>
                    <th style={{ padding: '10px' }}>Име</th>
                    <th style={{ padding: '10px' }}>Позиция</th>
                    <th style={{ padding: '10px' }}>Username</th>
                    <th style={{ padding: '10px' }}>Действия</th>
                </tr>
                </thead>
                <tbody>
                {employees.map(emp => (
                    <tr key={emp.id} style={{ borderBottom: '1px solid #ddd' }}>
                        <td style={{ padding: '8px' }}>{emp.first_name} {emp.last_name}</td>
                        <td style={{ padding: '8px' }}>{emp.work_position_name || emp.work_position}</td>
                        <td style={{ padding: '8px' }}>{emp.username || 'Няма акаунт'}</td>
                        <td style={{ padding: '8px' }}>
                            <button onClick={() => handleUpdateName(emp.id, emp.first_name)} style={{ cursor: 'pointer' }}>Edit</button>
                            <button
                                onClick={() => handleDelete(emp.id)}
                                style={{ color: 'red', marginLeft: '10px', cursor: 'pointer' }}
                            >
                                Delete
                            </button>
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>
            {employees.length === 0 && <p style={{ padding: '10px' }}>Няма намерени служители.</p>}
        </div>
    );
};

export default EmployeeList;
