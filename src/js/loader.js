/**
 * Loader Utility
 * Fetches HTML from a file and injects it into a DOM element
 */

const componentCache = new Map();

export async function loadComponent(path) {
    if (componentCache.has(path)) {
        return componentCache.get(path);
    }
    try {
        const response = await fetch(path);
        if (!response.ok) throw new Error(`Failed to load component: ${path}`);
        const html = await response.text();
        componentCache.set(path, html);
        return html;
    } catch (error) {
        console.error(error);
        return `<div class="p-4 text-red-500">Error loading component: ${path}</div>`;
    }
}

export async function injectComponent(path, targetElement) {
    const html = await loadComponent(path);
    if (targetElement) {
        targetElement.innerHTML = html;
    }
}
