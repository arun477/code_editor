import { useAuth } from '../contexts/AuthContext';
import { API_BASE_URL } from '../constants';

export const useApi = () => {
    const { user, logout } = useAuth();

    const callApi = async (endpoint, options = {}) => {
        const url = `${API_BASE_URL}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers,
        };

        if (user && user.token) {
            headers['Authorization'] = `Bearer ${user.token}`;
        }

        try {
            const response = await fetch(url, {
                ...options,
                headers,
            });

            if (response.status === 401) {
                const detail = await response.json();
                // Token is invalid or expired
                logout();
                throw new Error(detail.detail);
            }

            if (!response.ok) {
                throw new Error('An error occurred while fetching data');
            }

            return await response.json();
        } catch (error) {
            console.error('API call failed:', error);
            throw error;
        }
    };

    return { callApi };
};
