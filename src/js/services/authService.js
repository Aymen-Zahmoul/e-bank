/**
 * Authentication Service
 * Handles user login, logout, and session state
 */
export const authService = {
    login: async (email, password) => {
        // Mock login logic
        console.log('Logging in...', email);
        localStorage.setItem('user', JSON.stringify({ email, name: 'Alexander Thorne', tier: 'Private Wealth' }));
        return true;
    },
    
    sendVerificationCode: async (email) => {
        console.log(`Sending verification code to ${email}...`);
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        // In a real app, this would trigger a backend email
        // For demo, we'll use '123456' as the valid code
        localStorage.setItem('pending_email', email);
        return true;
    },

    verifyCode: async (email, code) => {
        console.log(`Verifying code ${code} for ${email}...`);
        await new Promise(resolve => setTimeout(resolve, 800));
        
        if (code === '123456') {
            localStorage.setItem('user', JSON.stringify({ 
                email, 
                name: email.split('@')[0], 
                tier: 'Standard' 
            }));
            localStorage.removeItem('pending_email');
            return true;
        }
        return false;
    },

    signup: async (userData) => {
        console.log('Signing up...', userData);
        await new Promise(resolve => setTimeout(resolve, 1200));
        localStorage.setItem('user', JSON.stringify({ 
            ...userData, 
            tier: 'Standard' 
        }));
        return true;
    },

    loginWithProvider: async (provider) => {
        console.log(`Logging in with ${provider}...`);
        // Simulate OAuth popup delay
        await new Promise(resolve => setTimeout(resolve, 1500));
        localStorage.setItem('user', JSON.stringify({ 
            email: `user@${provider}.com`, 
            name: `${provider} User`, 
            tier: 'Private Wealth' 
        }));
        return true;
    },

    logout: () => {
        localStorage.removeItem('user');
        window.location.hash = '#/login';
    },
    
    getCurrentUser: () => {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    },
    
    isAuthenticated: () => {
        return !!localStorage.getItem('user');
    }
};
