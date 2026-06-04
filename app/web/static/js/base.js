/**
 * BASE JS - Avery Production
 * Global utilities, navigation, accessibility
 */

(function() {
    'use strict';
    
    // DOM Elements
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarMenu = document.querySelector('.navbar-menu');
    const alerts = document.querySelectorAll('.alert');
    const userMenuBtn = document.querySelector('.user-menu-btn');
    const userDropdown = document.querySelector('.user-dropdown');
    
    // Mobile Navigation Toggle
    function initMobileNav() {
        if (!navbarToggler || !navbarMenu) return;
        
        navbarToggler.addEventListener('click', (e) => {
            e.stopPropagation();
            const expanded = navbarToggler.getAttribute('aria-expanded') === 'true';
            navbarToggler.setAttribute('aria-expanded', !expanded);
            navbarMenu.classList.toggle('active');
            document.body.style.overflow = navbarMenu.classList.contains('active') ? 'hidden' : '';
        });
        
        // Close menu on link click
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                navbarMenu.classList.remove('active');
                navbarToggler.setAttribute('aria-expanded', 'false');
                document.body.style.overflow = '';
            });
        });
        
        // Close menu on outside click
        document.addEventListener('click', (e) => {
            if (navbarMenu.classList.contains('active') && 
                !navbarMenu.contains(e.target) && 
                !navbarToggler.contains(e.target)) {
                navbarMenu.classList.remove('active');
                navbarToggler.setAttribute('aria-expanded', 'false');
                document.body.style.overflow = '';
            }
        });
    }
    
    // Auto-dismiss alerts
    function initAlerts() {
        alerts.forEach(alert => {
            const closeBtn = alert.querySelector('.alert-close');
            if (closeBtn) {
                closeBtn.addEventListener('click', () => {
                    alert.style.animation = 'slideUp 0.3s ease-out forwards';
                    setTimeout(() => alert.remove(), 300);
                });
            }
            
            // Auto-dismiss after 5 seconds
            setTimeout(() => {
                if (alert && alert.parentNode) {
                    alert.style.animation = 'slideUp 0.3s ease-out forwards';
                    setTimeout(() => alert.remove(), 300);
                }
            }, 5000);
        });
    }
    
    // User dropdown menu
    function initUserDropdown() {
        if (!userMenuBtn || !userDropdown) return;
        
        userMenuBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const expanded = userMenuBtn.getAttribute('aria-expanded') === 'true';
            userMenuBtn.setAttribute('aria-expanded', !expanded);
            userDropdown.hidden = expanded;
        });
        
        document.addEventListener('click', (e) => {
            if (!userDropdown.hidden && 
                !userDropdown.contains(e.target) && 
                !userMenuBtn.contains(e.target)) {
                userDropdown.hidden = true;
                userMenuBtn.setAttribute('aria-expanded', 'false');
            }
        });
    }
    
    // Set active navigation link
    function setActiveNavLink() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.nav-link');
        
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href === currentPath || 
                (currentPath === '/' && href === '/') ||
                (currentPath !== '/' && href !== '/' && currentPath.startsWith(href))) {
                link.classList.add('active');
                link.setAttribute('aria-current', 'page');
            } else {
                link.classList.remove('active');
                link.removeAttribute('aria-current');
            }
        });
    }
    
    // Performance monitoring
    function reportPerformance() {
        if ('performance' in window && 'getEntriesByType' in performance) {
            const navEntry = performance.getEntriesByType('navigation')[0];
            if (navEntry) {
                console.debug(`Page load time: ${navEntry.loadEventEnd - navEntry.startTime}ms`);
            }
        }
    }
    
    // CSRF token setup for AJAX requests
    function setupCSRF() {
        const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
        
        if (csrfToken && window.fetch) {
            const originalFetch = window.fetch;
            window.fetch = function(...args) {
                if (args[1] && args[1].method && 
                    ['POST', 'PUT', 'PATCH', 'DELETE'].includes(args[1].method.toUpperCase())) {
                    args[1].headers = {
                        ...args[1].headers,
                        'X-CSRF-Token': csrfToken
                    };
                }
                return originalFetch.apply(this, args);
            };
        }
    }
    
    // Handle service worker registration
    function registerServiceWorker() {
        if ('serviceWorker' in navigator && process.env.NODE_ENV === 'production') {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/sw.js')
                    .then(registration => {
                        console.debug('SW registered:', registration.scope);
                    })
                    .catch(error => {
                        console.debug('SW registration failed:', error);
                    });
            });
        }
    }
    
    // Smooth scroll for anchor links
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]:not([href="#"])').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const targetId = this.getAttribute('href');
                const target = document.querySelector(targetId);
                
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                    
                    // Update URL without jumping
                    history.pushState(null, null, targetId);
                }
            });
        });
    }
    
    // Add animation styles
    function addAnimationStyles() {
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideUp {
                from {
                    opacity: 1;
                    transform: translateY(0);
                }
                to {
                    opacity: 0;
                    transform: translateY(-20px);
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Initialize on DOM ready
    document.addEventListener('DOMContentLoaded', () => {
        initMobileNav();
        initAlerts();
        initUserDropdown();
        setActiveNavLink();
        setupCSRF();
        initSmoothScroll();
        addAnimationStyles();
        reportPerformance();
        
        // Register service worker in production
        if (document.location.hostname !== 'localhost') {
            registerServiceWorker();
        }
    });
    
    // Handle page visibility changes
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            console.debug('Page hidden');
        } else {
            console.debug('Page visible');
        }
    });
})();