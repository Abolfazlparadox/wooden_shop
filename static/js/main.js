// static/js/main.js

document.addEventListener('DOMContentLoaded', () => {

    // --- 1. Page Loader ---
    const loader = document.getElementById('loader-overlay');
    window.addEventListener('load', () => {
        if (loader) {
            loader.style.opacity = '0';
            setTimeout(() => {
                loader.style.display = 'none';
            }, 500); // Match the CSS transition duration
        }
    });

    // --- 2. Dark Mode Toggle ---
    const themeToggleBtn = document.getElementById('theme-toggle');
    const sunIcon = document.getElementById('theme-toggle-sun');
    const moonIcon = document.getElementById('theme-toggle-moon');
    const htmlElement = document.documentElement;

    // Apply the theme on initial load
    if (localStorage.getItem('theme') === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        htmlElement.classList.add('dark');
        if (sunIcon) sunIcon.classList.remove('hidden');
        if (moonIcon) moonIcon.classList.add('hidden');
    } else {
        htmlElement.classList.remove('dark');
        if (sunIcon) sunIcon.classList.add('hidden');
        if (moonIcon) moonIcon.classList.remove('hidden');
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            htmlElement.classList.toggle('dark');
            const isDark = htmlElement.classList.contains('dark');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');

            // Toggle icons
            if (sunIcon) sunIcon.classList.toggle('hidden', !isDark);
            if (moonIcon) moonIcon.classList.toggle('hidden', isDark);
        });
    }

    // --- 3. Mobile Sidebar Drawer ---
    const sidebar = document.getElementById('mobile-sidebar');
    const sidebarBackdrop = document.getElementById('sidebar-backdrop');
    const openSidebarBtn = document.getElementById('open-sidebar');
    const closeSidebarBtn = document.getElementById('close-sidebar');

    const toggleSidebar = () => {
        if (sidebar && sidebarBackdrop) {
            sidebar.classList.toggle('translate-x-full');
            sidebarBackdrop.classList.toggle('hidden');
        }
    };

    if (openSidebarBtn) openSidebarBtn.addEventListener('click', toggleSidebar);
    if (closeSidebarBtn) closeSidebarBtn.addEventListener('click', toggleSidebar);
    if (sidebarBackdrop) sidebarBackdrop.addEventListener('click', toggleSidebar);

});
