import { Router } from './router.js';
import { authService } from './services/authService.js';

const showAuthLoaderAndNavigate = (hash) => {
    const appElement = document.getElementById('app');
    if (appElement) {
        appElement.innerHTML = `
            <div class="ebanking-loader-container">
              <div class="css-credit-card">
                <div class="card-sweep"></div>
                
                <div class="card-chip"></div>
                
                <div class="card-contactless">
                  <span></span>
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
              
              <p class="loader-text">
                Authenticating<span>.</span><span>.</span><span>.</span>
              </p>
            </div>
        `;
    }
    setTimeout(() => {
        window.location.hash = hash;
    }, 2500);
};

const routes = {
    '#/': { view: '/src/views/landing.html', layout: 'landing' },
    '#/personal': { view: '/src/views/landing.html', layout: 'landing' },
    '#/business': { view: '/src/views/business.html', layout: 'landing' },
    '#/login': {  
        view: '/src/views/login.html', 
        layout: 'none',
        init: () => {
            const step1 = document.getElementById('login-step-1');
            const step2 = document.getElementById('login-step-2');
            const emailInput = document.getElementById('email');
            const codeInput = document.getElementById('code');
            const googleBtn = document.getElementById('google-login');
            const appleBtn = document.getElementById('apple-login');
            const changeEmailBtn = document.getElementById('change-email');

            if (step1) {
                step1.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const email = emailInput.value;
                    const btn = document.getElementById('send-code-btn');
                    btn.disabled = true;
                    btn.innerText = 'Sending...';
                    
                    await authService.sendVerificationCode(email);
                    
                    step1.classList.add('hidden');
                    step2.classList.remove('hidden');
                });
            }

            if (step2) {
                step2.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const email = emailInput.value;
                    const code = codeInput.value;
                    const btn = document.getElementById('verify-code-btn');
                    btn.disabled = true;
                    btn.innerText = 'Verifying...';

                    const success = await authService.verifyCode(email, code);
                    if (success) {
                        showAuthLoaderAndNavigate('#/dashboard');
                    } else {
                        alert('Invalid verification code. Please try again.');
                        btn.disabled = false;
                        btn.innerText = 'Verify & Sign In';
                    }
                });
            }

            if (changeEmailBtn) {
                changeEmailBtn.addEventListener('click', () => {
                    step2.classList.add('hidden');
                    step1.classList.remove('hidden');
                });
            }

            const handleProviderLogin = async (provider) => {
                // Realistic popup simulation
                const popup = window.open('', 'auth_popup', 'width=500,height=600,left=200,top=100');
                if (popup) {
                    popup.document.write(`
                        <html>
                            <head>
                                <title>Sign in with ${provider}</title>
                                <style>
                                    body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; background: #f8fafc; }
                                    .card { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); text-align: center; max-width: 320px; }
                                    .logo { font-size: 24px; font-weight: bold; margin-bottom: 20px; color: #00081e; }
                                    .loader { border: 3px solid #f3f3f3; border-top: 3px solid #005cab; border-radius: 50%; width: 24px; height: 24px; animation: spin 1s linear infinite; margin: 20px auto; }
                                    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
                                    .status { color: #64748b; font-size: 14px; }
                                </style>
                            </head>
                            <body>
                                <div class="card">
                                    <div class="logo">AUREX BANK</div>
                                    <div class="status">Connecting to ${provider}...</div>
                                    <div class="loader"></div>
                                    <div class="status">Authorizing account...</div>
                                </div>
                                <script>
                                    setTimeout(() => {
                                        window.close();
                                    }, 2000);
                                </script>
                            </body>
                        </html>
                    `);
                }

                const success = await authService.loginWithProvider(provider);
                if (success) showAuthLoaderAndNavigate('#/dashboard');
            };

            if (googleBtn) googleBtn.addEventListener('click', () => handleProviderLogin('Google'));
            if (appleBtn) appleBtn.addEventListener('click', () => handleProviderLogin('Apple'));
        }
    },
    '#/signup': { 
        view: '/src/views/signup.html', 
        layout: 'none',
        init: () => {
            const signupForm = document.getElementById('signup-form');
            if (signupForm) {
                signupForm.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const name = document.getElementById('full-name').value;
                    const email = document.getElementById('email').value;
                    const password = document.getElementById('password').value;
                    const btn = document.getElementById('signup-btn');
                    
                    btn.disabled = true;
                    btn.innerText = 'Creating Account...';

                    await authService.signup({ name, email, password });
                    showAuthLoaderAndNavigate('#/dashboard');
                });
            }
        }
    },
    '#/dashboard': { view: '/src/views/dashboard.html', layout: 'dashboard' },
    '#/transactions': { view: '/src/views/transactions.html', layout: 'dashboard' },
    '#/cards': { view: '/src/views/cards.html', layout: 'dashboard' },
    '#/loans': { view: '/src/views/loans.html', layout: 'dashboard' },
    '#/investment': { view: '/src/views/investment.html', layout: 'dashboard' },
    '#/profile': { view: '/src/views/profile.html', layout: 'dashboard' },
    '#/wealth-management': { view: '/src/views/wealth-management.html', layout: 'landing' },
    '#/about': { view: '/src/views/about.html', layout: 'landing' },
    '#/404': { view: '/src/views/404.html', layout: 'none' }
};

document.addEventListener('DOMContentLoaded', () => {
    const appElement = document.getElementById('app');
    new Router(routes, appElement);

    // Global event delegation for logout
    document.addEventListener('click', (e) => {
        const logoutBtn = e.target.closest('#logout-btn');
        if (logoutBtn) {
            e.preventDefault();
            authService.logout();
        }
    });
});
