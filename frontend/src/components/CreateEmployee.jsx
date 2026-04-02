import { useState, useEffect } from 'react';
import api from '../api.js';

const CreateEmployee = ({ onEmployeeAdded }) => {
    const [positions, setPositions] = useState([]);
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        clock_number: '',
        work_position: '',
        login_required: false
    });

    useEffect(() => {
        api.get('accounts/api/positions/')
            .then(res => {
                // ПРОВЕРКА: Ако Django връща пагинация, данните са в res.data.results
                // Ако не връща пагинация, са директно в res.data
                const data = res.data.results ? res.data.results : res.data;

                // Подсигуряваме се, че винаги записваме масив
                setPositions(Array.isArray(data) ? data : []);
            })
            .catch(err => console.error("Error loading positions:", err));
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await api.post('accounts/api/employees/', formData);

            alert(`Success! Employee created.`);

            // Изчистване на формата
            setFormData({
                first_name: '',
                last_name: '',
                clock_number: '',
                work_position: '',
                login_required: false
            });

            // Сигнализираме на родителя да обнови списъка
            if (onEmployeeAdded) {
                onEmployeeAdded();
            }
        } catch (err) {
            console.error("Error details:", err.response?.data);
            alert("Грешка при създаване! Проверете дали сте логнати или дали данните са коректни.");
        }
    };

    return (
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
            <input
                placeholder="First Name"
                value={formData.first_name}
                required
                style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
                onChange={e => setFormData({...formData, first_name: e.target.value})}
            />
            <input
                placeholder="Last Name"
                value={formData.last_name}
                required
                style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
                onChange={e => setFormData({...formData, last_name: e.target.value})}
            />
            <input
                placeholder="Clock Number"
                value={formData.clock_number}
                required
                style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
                onChange={e => setFormData({...formData, clock_number: e.target.value})}
            />

            <select
                value={formData.work_position}
                required
                style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
                onChange={e => setFormData({...formData, work_position: e.target.value})}
            >
                <option value="">Select Work Position</option>
                {/* Тук positions вече гарантирано е масив благодарение на проверката в useEffect */}
                {positions.map(pos => (
                    <option key={pos.id} value={pos.id}>{pos.name}</option>
                ))}
            </select>

            <label style={{ cursor: 'pointer', fontSize: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <input
                    type="checkbox"
                    checked={formData.login_required}
                    onChange={e => setFormData({...formData, login_required: e.target.checked})}
                />
                Is Login Required?
            </label>

            <button type="submit" style={{ padding: '10px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}>
                Add Employee
            </button>
        </form>
    );
};

export default CreateEmployee;
