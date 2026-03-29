import { loadComponent } from './loader.js';
import { authService } from './services/authService.js';

/**
 * Advanced Router
 * Handles dynamic rendering, Route Guards, layout persistence, and page transitions
 */
export class Router {
    constructor(routes, appElement) {
        this.routes = routes;
        this.appElement = appElement;
        this.currentLayout = null; // Track current layout to prevent re-rendering
        this.init();
    }

    init() {
        window.addEventListener('hashchange', () => this.handleRouteChange());
        window.addEventListener('load', () => this.handleRouteChange());
    }

    async handleRouteChange() {
        const hash = window.location.hash || '#/';
        const route = this.routes[hash] || this.routes['#/404'];

        if (!route) return;

        // Route Guard: Protected Routes
        const isAuthenticated = authService.isAuthenticated();
        if (route.layout === 'dashboard' && !isAuthenticated) {
            this.navigate('#/login');
            return;
        }
        
        // Route Guard: Prevent logged-in users from seeing login/signup
        if ((hash === '#/login' || hash === '#/signup') && isAuthenticated) {
            this.navigate('#/dashboard');
            return;
        }

        // Load view
        const viewHtml = await loadComponent(route.view);
        
        // Handle Persistent Layouts
        if (this.currentLayout !== route.layout) {
            this.currentLayout = route.layout;
            
            if (route.layout === 'dashboard') {
                const sidebarHtml = await loadComponent('/src/components/sidebar.html');
                this.appElement.innerHTML = `
                    <div class="with-sidebar">
                        ${sidebarHtml}
                        <div class="content-area">
                            <div id="view-container" class="page-transition opacity-0">${viewHtml}</div>
                        </div>
                    </div>
                `;
            } else if (route.layout === 'landing') {
                const navbarHtml = await loadComponent('/src/components/navbar.html');
                const footerHtml = await loadComponent('/src/components/footer.html');
                this.appElement.innerHTML = `
                    ${navbarHtml}
                    <main id="view-container" class="main-content page-transition opacity-0">${viewHtml}</main>
                    ${footerHtml}
                `;
            } else {
                this.appElement.innerHTML = `<div id="view-container" class="page-transition opacity-0">${viewHtml}</div>`;
            }
        } else {
            // Layout is already matching, just replace the inner content
            const container = document.getElementById('view-container');
            if (container) {
                container.classList.remove('fade-in');
                // Await a tiny bit to allow the fade-out class to register
                await new Promise(resolve => setTimeout(resolve, 50));
                container.innerHTML = viewHtml;
            }
        }

        // Execute view-specific scripts if any (now that DOM is updated)
        if (route.init) route.init();

        // Trigger Fade-In Transition
        setTimeout(() => {
            const container = document.getElementById('view-container');
            if (container) {
                container.classList.add('fade-in');
            }
        }, 50);
        
        // Update active links
        this.updateActiveLinks(hash);
    }

    updateActiveLinks(hash) {
        document.querySelectorAll('a[href]').forEach(link => {
            if (link.getAttribute('href') === hash) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }

    navigate(hash) {
        window.location.hash = hash;
    }
}
