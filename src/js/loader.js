/**
 * Loader Utility
 * Fetches HTML from a file and injects it into a DOM element
 */
export async function loadComponent(path) {
    try {
        const response = await fetch(path);
        if (!response.ok) throw new Error(`Failed to load component: ${path}`);
        return await response.text();
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
