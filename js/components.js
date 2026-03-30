
// Component Loader
async function loadComponent(elementId, componentPath) {
    try {
        const response = await fetch(componentPath);
        if (!response.ok) throw new Error('Network response was not ok');
        const html = await response.text();
        const el = document.getElementById(elementId);
        if (el) {
            el.innerHTML = html;
        }
    } catch (error) {
        console.error(`Failed to load component ${componentPath}:`, error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Determine path depth based on location
    const isRoot = window.location.pathname.endsWith('index.html') || window.location.pathname === '/' || window.location.pathname.indexOf('/') === -1;
    const componentPrefix = isRoot ? 'components/' : '../components/';
    
    if (document.getElementById('navbar')) {
        loadComponent('navbar', componentPrefix + 'navbar.html');
    }
    if (document.getElementById('sidebar')) {
        loadComponent('sidebar', componentPrefix + 'sidebar.html');
    }
    if (document.getElementById('admin-sidebar')) {
        loadComponent('admin-sidebar', componentPrefix + 'admin-sidebar.html');
    }
    if (document.getElementById('footer')) {
        loadComponent('footer', componentPrefix + 'footer.html');
    }
});
