import axios from 'axios';
//тук се задава основният url
const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/',
    withCredentials: true,
});
//прохващане на заявките и защитата им с токен - предпазва от CSRF атаки.
api.interceptors.request.use((config) => {
    const getCookie = (name) => {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {      //тази функция търси кукитата и връща тази, която е според зададените критерии
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    const csrfToken = getCookie('csrftoken');    // тук вика горната функция с параметър име на бисквитката
    if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken;   // слага необходимта стойност в хедъра
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

// Добавяме функцията logout, която Sidebar очаква
export const logout = () => {
    // Използваме localStorage.clear() за всеки случай
    localStorage.clear();
    // Пренасочваме към стандартния Django logout адрес
    window.location.href = 'http://127.0.0.1:8000/accounts/logout/';
};

export default api;
