import { loadComponent } from './loader.js';

/**
 * Simple Router
 * Detects route changes and loads the correct view dynamically
 */
export class Router {
    constructor(routes, appElement) {
        this.routes = routes;
        this.appElement = appElement;
        this.init();
    }

    init() {
        window.addEventListener('hashchange', () => this.handleRouteChange());
        window.addEventListener('load', () => this.handleRouteChange());
    }

    async handleRouteChange() {
        const hash = window.location.hash || '#/';
        const route = this.routes[hash] || this.routes['#/404'];

        if (route) {
            // Load view
            const viewHtml = await loadComponent(route.view);
            
            // If the route requires a layout (navbar/sidebar), we handle it here
            if (route.layout === 'dashboard') {
                const sidebarHtml = await loadComponent('/src/components/sidebar.html');
                this.appElement.innerHTML = `
                    <div class="with-sidebar">
                        ${sidebarHtml}
                        <div class="content-area">
                            <div id="view-container">${viewHtml}</div>
                        </div>
                    </div>
                `;
            } else if (route.layout === 'landing') {
                const navbarHtml = await loadComponent('/src/components/navbar.html');
                const footerHtml = await loadComponent('/src/components/footer.html');
                this.appElement.innerHTML = `
                    ${navbarHtml}
                    <main class="main-content">${viewHtml}</main>
                    ${footerHtml}
                `;
            } else {
                this.appElement.innerHTML = viewHtml;
            }

            // Execute view-specific scripts if any
            if (route.init) route.init();
            
            // Update active links
            this.updateActiveLinks(hash);
        }
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
