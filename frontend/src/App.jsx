import { useState } from 'react';
import CreateEmployee from './components/CreateEmployee.jsx';
import EmployeeList from './components/EmployeeList.jsx';

function App() {
    // Състояние за обновяване на списъка
    const [refreshKey, setRefreshKey] = useState(0);

    const handleEmployeeAdded = () => {
        setRefreshKey(prev => prev + 1);
    };

    const handleHome = () => {
        window.location.href = 'http://127.0.0.1:8000/';
    };

    return (
        <div style={{ minHeight: '100vh', backgroundColor: '#f4f7f6', fontFamily: 'Arial, sans-serif' }}>
            <header style={{ 
                backgroundColor: '#ffffff', 
                padding: '10px 20px', 
                borderBottom: '1px solid #ddd',
                display: 'flex',
                alignItems: 'center',
                boxShadow: '0 2px 4px rgba(0,0,0,0.05)'
            }}>
                <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
                    <button onClick={handleHome} style={{ padding: '8px 15px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}>
                        🏠 Home
                    </button>
                    <h2 style={{ margin: 0, color: '#333' }}>HR Management</h2>
                </div>
            </header>

            <main style={{ padding: '40px 20px', maxWidth: '1000px', margin: '0 auto' }}>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 2.5fr', gap: '30px' }}>
                    <section style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)', height: 'fit-content' }}>
                        <h3 style={{ marginTop: 0 }}>Add New Employee</h3>
                        <CreateEmployee onEmployeeAdded={handleEmployeeAdded} />
                    </section>

                    <section style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>
                        <h3 style={{ marginTop: 0 }}>Existing Employees</h3>
                        <EmployeeList key={refreshKey} />
                    </section>
                </div>
            </main>
        </div>
    );
}

export default App;
