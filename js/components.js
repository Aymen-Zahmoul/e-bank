
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

function initPageTransitions() {
    // Initial fade in for harmony
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.4s ease-in-out';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 10);

    // Intercept internal links for smooth fade out
    document.body.addEventListener('click', (e) => {
        const link = e.target.closest('a');
        if (link) {
            const href = link.getAttribute('href');
            const target = link.getAttribute('target');
            
            // Only intercept valid internal links
            if (href && !href.startsWith('http') && !href.startsWith('#') && !href.startsWith('mailto:') && target !== '_blank' && !link.hasAttribute('download')) {
                e.preventDefault();
                document.body.style.opacity = '0';
                setTimeout(() => {
                    window.location.href = href;
                }, 400); // Wait for transition to complete before navigating
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    initPageTransitions();
    
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
