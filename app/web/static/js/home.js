/**
 * HOME JS - Avery Production
 * Home page specific functionality
 */

(function() {
    'use strict';
    
    // Stats animation with Intersection Observer
    function initStatsAnimation() {
        const statsContainer = document.getElementById('stats-container');
        if (!statsContainer) return;
        
        // Sample stats data - replace with API call
        const stats = [
            { number: '10K+', label: 'Active Users' },
            { number: '99.9%', label: 'Uptime' },
            { number: '<50ms', label: 'Response Time' },
            { number: '24/7', label: 'Support' }
        ];
        
        const statsHTML = `
            <div class="stats-grid">
                ${stats.map(stat => `
                    <div class="stat-item">
                        <span class="stat-number" data-count="${stat.number}">0</span>
                        <span class="stat-label">${stat.label}</span>
                    </div>
                `).join('')}
            </div>
        `;
        
        statsContainer.innerHTML = statsHTML;
        
        // Animate numbers when visible
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const statNumbers = entry.target.querySelectorAll('.stat-number');
                    statNumbers.forEach(stat => {
                        const targetValue = stat.getAttribute('data-count');
                        animateNumber(stat, targetValue);
                    });
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        observer.observe(statsContainer);
    }
    
    // Number animation
    function animateNumber(element, target) {
        const isPercentage = target.includes('%');
        const isTime = target.includes('ms');
        const isPlus = target.includes('+');
        
        let numericValue = parseInt(target);
        if (isNaN(numericValue)) {
            element.textContent = target;
            return;
        }
        
        let start = 0;
        const duration = 2000;
        const increment = numericValue / (duration / 16);
        
        const updateNumber = () => {
            start += increment;
            if (start < numericValue) {
                let displayValue = Math.floor(start);
                if (isPercentage) displayValue += '%';
                else if (isTime) displayValue += 'ms';
                else if (isPlus) displayValue += '+';
                element.textContent = displayValue;
                requestAnimationFrame(updateNumber);
            } else {
                element.textContent = target;
            }
        };
        
        requestAnimationFrame(updateNumber);
    }
    
    // Feature card hover effects
    function initFeatureCards() {
        const cards = document.querySelectorAll('.feature-card');
        
        cards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                const icon = card.querySelector('.feature-icon');
                if (icon) {
                    icon.style.animation = 'none';
                    icon.offsetHeight; // Trigger reflow
                    icon.style.animation = 'float 3s ease-in-out infinite';
                }
            });
            
            // Add loading state simulation
            card.addEventListener('click', async (e) => {
                if (!card.classList.contains('loading')) {
                    card.classList.add('loading');
                    // Simulate API call
                    await new Promise(resolve => setTimeout(resolve, 500));
                    card.classList.remove('loading');
                }
            });
        });
    }
    
    // Newsletter subscription form
    function initSubscriptionForm() {
        const form = document.getElementById('subscribe-form');
        const messageDiv = document.getElementById('form-message');
        
        if (!form || !messageDiv) return;
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(form);
            const email = formData.get('email');
            
            // Basic email validation
            if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
                showMessage('Please enter a valid email address.', 'error');
                return;
            }
            
            // Disable form during submission
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.disabled = true;
            submitBtn.textContent = 'Subscribing...';
            
            try {
                // Replace with your actual API endpoint
                const response = await fetch('/subscribe', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: JSON.stringify({ email })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    showMessage('Successfully subscribed! Check your email for confirmation.', 'success');
                    form.reset();
                } else {
                    showMessage(data.message || 'Subscription failed. Please try again.', 'error');
                }
            } catch (error) {
                console.error('Subscription error:', error);
                showMessage('Network error. Please check your connection and try again.', 'error');
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
            }
        });
    }
    
    // Message display helper
    function showMessage(message, type) {
        const messageDiv = document.getElementById('form-message');
        if (!messageDiv) return;
        
        messageDiv.textContent = message;
        messageDiv.className = `form-message message-${type}`;
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            messageDiv.textContent = '';
            messageDiv.className = 'form-message';
        }, 5000);
    }
    
    // Lazy load images
    function initLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.add('loaded');
                        observer.unobserve(img);
                    }
                });
            });
            
            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }
    
    // Track user interactions (analytics)
    function trackInteractions() {
        const trackEvent = (category, action, label) => {
            // Replace with your analytics implementation
            if (typeof gtag !== 'undefined') {
                gtag('event', action, {
                    'event_category': category,
                    'event_label': label
                });
            }
            console.debug(`Analytics: ${category} - ${action} - ${label}`);
        };
        
        // Track CTA button clicks
        document.querySelectorAll('.hero-buttons .btn').forEach(btn => {
            btn.addEventListener('click', () => {
                trackEvent('CTA', 'click', btn.textContent);
            });
        });
        
        // Track feature card clicks
        document.querySelectorAll('.feature-card').forEach(card => {
            card.addEventListener('click', () => {
                const feature = card.querySelector('h3')?.textContent;
                trackEvent('Feature', 'click', feature);
            });
        });
    }
    
    // Add scroll reveal animations
    function initScrollReveal() {
        const revealElements = document.querySelectorAll('.feature-card, .hero-stats');
        
        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '50px' });
        
        revealElements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            revealObserver.observe(el);
        });
    }
    
    // Performance monitoring for home page
    function monitorHomePagePerformance() {
        if ('performance' in window && 'getEntriesByType' in performance) {
            const paintEntries = performance.getElementsByType('paint');
            paintEntries.forEach(entry => {
                if (entry.name === 'first-contentful-paint') {
                    console.debug(`FCP: ${entry.startTime}ms`);
                }
            });
        }
    }
    
    // Initialize all home page features
    document.addEventListener('DOMContentLoaded', () => {
        initStatsAnimation();
        initFeatureCards();
        initSubscriptionForm();
        initLazyLoading();
        trackInteractions();
        initScrollReveal();
        monitorHomePagePerformance();
        
        // Log page view
        console.debug('Home page initialized');
    });
    
    // Handle page visibility for stats reset
    document.addEventListener('visibilitychange', () => {
        if (!document.hidden) {
            // Re-animate stats if they exist and are visible
            const statsContainer = document.getElementById('stats-container');
            if (statsContainer && statsContainer.querySelector('.stats-grid')) {
                const statNumbers = statsContainer.querySelectorAll('.stat-number');
                statNumbers.forEach(stat => {
                    const targetValue = stat.getAttribute('data-count');
                    if (targetValue && parseInt(targetValue) > 0 && stat.textContent === '0') {
                        animateNumber(stat, targetValue);
                    }
                });
            }
        }
    });
})();