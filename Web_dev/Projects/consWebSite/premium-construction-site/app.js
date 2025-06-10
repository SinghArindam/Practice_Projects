// Premium Construction Website JavaScript
// Author: SkyLine Construction Group
// Version: 1.0.0

class SkyLineWebsite {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initLoader();
        this.initCustomCursor();
        this.initScrollAnimations();
        this.initParallaxEffects();
        this.initNavigationMenu();
        this.initPortfolioFilter();
        this.initTestimonialsSlider();
        this.initContactForm();
        this.initStatsCounter();
        this.initParticleSystem();
        this.initHoverEffects();
        this.initSmoothScrolling();
        this.initHeaderScrollEffect();
        this.initKineticTypography();
    }

    setupEventListeners() {
        window.addEventListener('load', () => this.handlePageLoad());
        window.addEventListener('scroll', () => this.handleScroll());
        window.addEventListener('resize', () => this.handleResize());
        document.addEventListener('mousemove', (e) => this.updateCustomCursor(e));
    }

    // Page Loader with Construction Theme
    initLoader() {
        const loader = document.querySelector('.loader');
        const progressBar = document.querySelector('.loader-progress-bar');
        const counter = document.querySelector('.loader-counter');
        
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 100) progress = 100;
            
            progressBar.style.transform = `translateX(${progress - 100}%)`;
            counter.textContent = `${Math.floor(progress)}%`;
            
            if (progress === 100) {
                clearInterval(interval);
                setTimeout(() => {
                    loader.classList.add('loaded');
                    this.initHeroAnimations();
                }, 500);
            }
        }, 100);
    }

    handlePageLoad() {
        // Additional page load logic
        this.createParticles();
        this.initializeAllAnimations();
    }

    // Custom Cursor Effects
    initCustomCursor() {
        const cursorDot = document.querySelector('.cursor-dot');
        const cursorOutline = document.querySelector('.cursor-outline');
        
        if (!cursorDot || !cursorOutline) return;

        // Hide cursors on touch devices
        if ('ontouchstart' in window) {
            cursorDot.style.display = 'none';
            cursorOutline.style.display = 'none';
            return;
        }

        this.setupCursorInteractions(cursorDot, cursorOutline);
    }

    updateCustomCursor(e) {
        const cursorDot = document.querySelector('.cursor-dot');
        const cursorOutline = document.querySelector('.cursor-outline');
        
        if (!cursorDot || !cursorOutline) return;

        const posX = e.clientX;
        const posY = e.clientY;

        cursorDot.style.left = `${posX}px`;
        cursorDot.style.top = `${posY}px`;

        cursorOutline.style.left = `${posX}px`;
        cursorOutline.style.top = `${posY}px`;
    }

    setupCursorInteractions(dot, outline) {
        const interactiveElements = document.querySelectorAll('a, button, .service-card, .portfolio-card, .team-member');
        
        interactiveElements.forEach(el => {
            el.addEventListener('mouseenter', () => {
                dot.style.transform = 'scale(1.5)';
                outline.style.transform = 'scale(2)';
                outline.style.borderColor = '#ff6b35';
            });
            
            el.addEventListener('mouseleave', () => {
                dot.style.transform = 'scale(1)';
                outline.style.transform = 'scale(1)';
                outline.style.borderColor = '#ff6b35';
            });
        });
    }

    // Hero Section Animations
    initHeroAnimations() {
        const heroTitle = document.querySelector('.hero-title');
        const heroSubtitle = document.querySelector('.hero-subtitle');
        const heroCta = document.querySelector('.hero-cta');

        // Kinetic Typography for hero title
        if (heroTitle) {
            this.animateWords(heroTitle);
        }

        // Reveal subtitle and CTA
        setTimeout(() => {
            if (heroSubtitle) heroSubtitle.style.animation = 'fadeInUp 1s ease forwards';
        }, 1200);

        setTimeout(() => {
            if (heroCta) heroCta.style.animation = 'fadeInUp 1s ease forwards';
        }, 1600);
    }

    animateWords(element) {
        const words = element.querySelectorAll('.word');
        words.forEach((word, index) => {
            setTimeout(() => {
                word.style.animation = 'wordReveal 0.8s ease forwards';
            }, index * 200);
        });
    }

    // Kinetic Typography Effects
    initKineticTypography() {
        const titles = document.querySelectorAll('.section-title, .title-accent');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateLetters(entry.target);
                }
            });
        }, { threshold: 0.5 });

        titles.forEach(title => observer.observe(title));
    }

    animateLetters(element) {
        const text = element.textContent;
        element.innerHTML = '';
        
        [...text].forEach((letter, index) => {
            const span = document.createElement('span');
            span.textContent = letter === ' ' ? '\u00A0' : letter;
            span.style.display = 'inline-block';
            span.style.opacity = '0';
            span.style.transform = 'translateY(50px) rotateX(90deg)';
            span.style.transition = 'all 0.5s ease';
            span.style.transitionDelay = `${index * 0.05}s`;
            
            element.appendChild(span);
            
            setTimeout(() => {
                span.style.opacity = '1';
                span.style.transform = 'translateY(0) rotateX(0)';
            }, 100);
        });
    }

    // Scroll-triggered Animations
    initScrollAnimations() {
        const animateElements = document.querySelectorAll('.scroll-animate');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate');
                    this.triggerSpecialAnimations(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        animateElements.forEach(el => observer.observe(el));
    }

    triggerSpecialAnimations(element) {
        // Service cards 3D rotation
        if (element.classList.contains('service-card')) {
            element.style.animation = 'slideInUp 0.8s ease forwards';
        }
        
        // Team members staggered animation
        if (element.classList.contains('team-member')) {
            const index = Array.from(element.parentNode.children).indexOf(element);
            element.style.animationDelay = `${index * 0.2}s`;
            element.style.animation = 'fadeInUp 0.8s ease forwards';
        }
        
        // Portfolio items with morphing effects
        if (element.classList.contains('portfolio-item')) {
            element.style.animation = 'portfolioReveal 1s ease forwards';
        }
    }

    // Parallax Effects
    initParallaxEffects() {
        const parallaxElements = document.querySelectorAll('.parallax-element, .parallax-bg');
        
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            
            parallaxElements.forEach(element => {
                if (element.classList.contains('parallax-element')) {
                    element.style.transform = `translateY(${rate * 0.5}px)`;
                } else {
                    element.style.transform = `translateY(${rate}px)`;
                }
            });
        });
    }

    // Navigation Menu with Smooth Transitions
    initNavigationMenu() {
        const menuToggle = document.querySelector('.menu-toggle');
        const mainNav = document.querySelector('.main-nav');
        const navLinks = document.querySelectorAll('.nav-link');

        if (menuToggle) {
            menuToggle.addEventListener('click', () => {
                menuToggle.classList.toggle('active');
                mainNav.classList.toggle('active');
                document.body.style.overflow = mainNav.classList.contains('active') ? 'hidden' : '';
            });
        }

        // Smooth page transitions
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href');
                this.smoothScrollTo(targetId);
                
                // Close mobile menu
                if (mainNav.classList.contains('active')) {
                    menuToggle.classList.remove('active');
                    mainNav.classList.remove('active');
                    document.body.style.overflow = '';
                }
                
                // Update active state
                navLinks.forEach(l => l.classList.remove('active'));
                link.classList.add('active');
            });
        });
    }

    // Smooth Scrolling
    initSmoothScrolling() {
        const links = document.querySelectorAll('a[href^="#"]');
        
        links.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href');
                this.smoothScrollTo(targetId);
            });
        });
    }

    smoothScrollTo(targetId) {
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            const headerHeight = document.querySelector('.site-header').offsetHeight;
            const targetPosition = targetElement.offsetTop - headerHeight;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    }

    // Header Scroll Effect
    initHeaderScrollEffect() {
        const header = document.querySelector('.site-header');
        let lastScrollY = 0;
        
        window.addEventListener('scroll', () => {
            const currentScrollY = window.scrollY;
            
            if (currentScrollY > 100) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
            
            // Hide/show header based on scroll direction
            if (currentScrollY > lastScrollY && currentScrollY > 200) {
                header.style.transform = 'translateY(-100%)';
            } else {
                header.style.transform = 'translateY(0)';
            }
            
            lastScrollY = currentScrollY;
        });
    }

    // Portfolio Filter with Liquid Transitions
    initPortfolioFilter() {
        const filterBtns = document.querySelectorAll('.filter-btn');
        const portfolioItems = document.querySelectorAll('.portfolio-item');

        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const filter = btn.getAttribute('data-filter');
                
                // Update active button
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                // Filter items with morphing animation
                portfolioItems.forEach((item, index) => {
                    const category = item.getAttribute('data-category');
                    const shouldShow = filter === 'all' || category === filter;
                    
                    setTimeout(() => {
                        if (shouldShow) {
                            item.classList.remove('hidden');
                            item.style.animation = 'morphIn 0.6s ease forwards';
                        } else {
                            item.classList.add('hidden');
                            item.style.animation = 'morphOut 0.6s ease forwards';
                        }
                    }, index * 50);
                });
            });
        });
    }

    // Testimonials Slider with 3D Effects
    initTestimonialsSlider() {
        const testimonials = document.querySelectorAll('.testimonial-item');
        const prevBtn = document.querySelector('.prev-btn');
        const nextBtn = document.querySelector('.next-btn');
        const dotsContainer = document.querySelector('.testimonial-dots');
        
        if (testimonials.length === 0) return;

        let currentIndex = 0;
        
        // Create dots
        testimonials.forEach((_, index) => {
            const dot = document.createElement('div');
            dot.classList.add('dot');
            if (index === 0) dot.classList.add('active');
            dot.addEventListener('click', () => this.goToTestimonial(index));
            dotsContainer.appendChild(dot);
        });

        // Navigation buttons
        if (prevBtn) prevBtn.addEventListener('click', () => this.previousTestimonial());
        if (nextBtn) nextBtn.addEventListener('click', () => this.nextTestimonial());

        // Auto-play
        setInterval(() => this.nextTestimonial(), 5000);

        // Store references for slider methods
        this.testimonials = testimonials;
        this.currentTestimonialIndex = currentIndex;
        this.dots = document.querySelectorAll('.dot');
    }

    goToTestimonial(index) {
        this.testimonials[this.currentTestimonialIndex].classList.remove('active');
        this.dots[this.currentTestimonialIndex].classList.remove('active');
        
        this.currentTestimonialIndex = index;
        
        this.testimonials[this.currentTestimonialIndex].classList.add('active');
        this.dots[this.currentTestimonialIndex].classList.add('active');
    }

    nextTestimonial() {
        const nextIndex = (this.currentTestimonialIndex + 1) % this.testimonials.length;
        this.goToTestimonial(nextIndex);
    }

    previousTestimonial() {
        const prevIndex = this.currentTestimonialIndex === 0 
            ? this.testimonials.length - 1 
            : this.currentTestimonialIndex - 1;
        this.goToTestimonial(prevIndex);
    }

    // Stats Counter Animation
    initStatsCounter() {
        const statNumbers = document.querySelectorAll('.stat-number');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        statNumbers.forEach(stat => observer.observe(stat));
    }

    animateCounter(element) {
        const target = parseInt(element.getAttribute('data-count'));
        const duration = 2000;
        const increment = target / (duration / 16);
        let current = 0;

        const updateCounter = () => {
            current += increment;
            if (current < target) {
                element.textContent = Math.floor(current);
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent = target;
                if (element.textContent === '98') {
                    element.textContent += '%';
                }
            }
        };

        updateCounter();
    }

    // Particle System for Background
    initParticleSystem() {
        this.createParticles();
        this.animateParticles();
    }

    createParticles() {
        const container = document.querySelector('.particle-container');
        if (!container) return;

        const particleCount = 50;
        
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.classList.add('particle');
            particle.style.cssText = `
                position: absolute;
                width: 2px;
                height: 2px;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                pointer-events: none;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
                animation: float ${3 + Math.random() * 4}s ease-in-out infinite;
                animation-delay: ${Math.random() * 2}s;
            `;
            container.appendChild(particle);
        }
    }

    animateParticles() {
        const style = document.createElement('style');
        style.textContent = `
            @keyframes float {
                0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0.3; }
                50% { transform: translateY(-20px) rotate(180deg); opacity: 1; }
            }
            @keyframes morphIn {
                from { opacity: 0; transform: scale(0.8) rotateY(90deg); }
                to { opacity: 1; transform: scale(1) rotateY(0deg); }
            }
            @keyframes morphOut {
                from { opacity: 1; transform: scale(1) rotateY(0deg); }
                to { opacity: 0; transform: scale(0.8) rotateY(-90deg); }
            }
            @keyframes portfolioReveal {
                from { opacity: 0; transform: translateY(30px) rotateX(45deg); }
                to { opacity: 1; transform: translateY(0) rotateX(0deg); }
            }
            @keyframes slideInUp {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }
        `;
        document.head.appendChild(style);
    }

    // Contact Form with Advanced Validation
    initContactForm() {
        const form = document.getElementById('contactForm');
        const successMessage = document.querySelector('.form-success-message');
        const resetBtn = document.querySelector('.reset-form');

        if (!form) return;

        // Real-time validation
        const inputs = form.querySelectorAll('.form-control');
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearFieldError(input));
        });

        // Form submission
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            if (this.validateForm(form)) {
                this.submitForm(form, successMessage);
            }
        });

        // Reset form
        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                successMessage.classList.remove('show');
                form.reset();
                this.clearAllErrors(form);
            });
        }
    }

    validateField(field) {
        const value = field.value.trim();
        const fieldName = field.name;
        let isValid = true;
        let message = '';

        // Reset field state
        field.classList.remove('error', 'success');

        switch (fieldName) {
            case 'name':
                if (!value) {
                    isValid = false;
                    message = 'Name is required';
                } else if (value.length < 2) {
                    isValid = false;
                    message = 'Name must be at least 2 characters';
                }
                break;
            case 'email':
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!value) {
                    isValid = false;
                    message = 'Email is required';
                } else if (!emailRegex.test(value)) {
                    isValid = false;
                    message = 'Please enter a valid email address';
                }
                break;
            case 'phone':
                if (value && !/^[\+]?[\d\s\-\(\)]+$/.test(value)) {
                    isValid = false;
                    message = 'Please enter a valid phone number';
                }
                break;
            case 'message':
                if (!value) {
                    isValid = false;
                    message = 'Message is required';
                } else if (value.length < 10) {
                    isValid = false;
                    message = 'Message must be at least 10 characters';
                }
                break;
        }

        // Update field state
        field.classList.add(isValid ? 'success' : 'error');
        this.showFieldFeedback(field, message, isValid);

        return isValid;
    }

    validateForm(form) {
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;

        requiredFields.forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
            }
        });

        return isValid;
    }

    showFieldFeedback(field, message, isValid) {
        const feedback = field.parentNode.querySelector('.form-feedback');
        if (feedback) {
            feedback.textContent = message;
            feedback.classList.remove('error', 'success', 'show');
            if (message) {
                feedback.classList.add(isValid ? 'success' : 'error', 'show');
            }
        }
    }

    clearFieldError(field) {
        field.classList.remove('error');
        const feedback = field.parentNode.querySelector('.form-feedback');
        if (feedback && feedback.classList.contains('error')) {
            feedback.classList.remove('show');
        }
    }

    clearAllErrors(form) {
        const fields = form.querySelectorAll('.form-control');
        fields.forEach(field => {
            field.classList.remove('error', 'success');
            const feedback = field.parentNode.querySelector('.form-feedback');
            if (feedback) {
                feedback.classList.remove('show', 'error', 'success');
                feedback.textContent = '';
            }
        });
    }

    submitForm(form, successMessage) {
        const submitBtn = form.querySelector('button[type="submit"]');
        const btnText = submitBtn.querySelector('.btn-text');
        const btnIcon = submitBtn.querySelector('.btn-icon');

        // Animate button
        submitBtn.disabled = true;
        btnText.textContent = 'Sending...';
        btnIcon.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

        // Simulate form submission
        setTimeout(() => {
            form.style.animation = 'morphOut 0.5s ease forwards';
            
            setTimeout(() => {
                successMessage.classList.add('show');
                successMessage.style.animation = 'morphIn 0.5s ease forwards';
            }, 500);

            // Reset button
            submitBtn.disabled = false;
            btnText.textContent = 'Send Message';
            btnIcon.innerHTML = '<i class="fas fa-paper-plane"></i>';
        }, 2000);
    }

    // Hover Effects and Micro-interactions
    initHoverEffects() {
        // Service cards 3D hover
        const serviceCards = document.querySelectorAll('.service-card');
        serviceCards.forEach(card => {
            card.addEventListener('mouseenter', (e) => {
                this.create3DHoverEffect(e.target);
            });
            
            card.addEventListener('mouseleave', (e) => {
                this.reset3DHoverEffect(e.target);
            });
        });

        // Button hover animations
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(btn => {
            btn.addEventListener('mouseenter', () => {
                btn.style.animation = 'buttonHover 0.3s ease forwards';
            });
        });

        // Image mask reveals
        const portfolioCards = document.querySelectorAll('.portfolio-card');
        portfolioCards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                const overlay = card.querySelector('.image-overlay');
                if (overlay) {
                    overlay.style.animation = 'overlayReveal 0.5s ease forwards';
                }
            });
        });
    }

    create3DHoverEffect(element) {
        element.style.transform = 'perspective(1000px) rotateX(10deg) rotateY(10deg) translateZ(20px)';
        element.style.boxShadow = '0 25px 50px rgba(0,0,0,0.2)';
    }

    reset3DHoverEffect(element) {
        element.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0px)';
        element.style.boxShadow = '';
    }

    // Scroll handling
    handleScroll() {
        this.updateScrollProgress();
        this.updateActiveNavLink();
    }

    updateScrollProgress() {
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        
        // Update any progress indicators
        const progressBars = document.querySelectorAll('.scroll-progress');
        progressBars.forEach(bar => {
            bar.style.width = scrolled + '%';
        });
    }

    updateActiveNavLink() {
        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('.nav-link');
        
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (pageYOffset >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    }

    // Window resize handling
    handleResize() {
        this.updateParticlePositions();
        this.recalculateAnimations();
    }

    updateParticlePositions() {
        const particles = document.querySelectorAll('.particle');
        particles.forEach(particle => {
            particle.style.left = Math.random() * 100 + '%';
        });
    }

    recalculateAnimations() {
        // Recalculate any position-dependent animations
        const animatedElements = document.querySelectorAll('.scroll-animate');
        animatedElements.forEach(el => {
            // Reset and recalculate intersection observer
            el.classList.remove('animate');
        });
    }

    // Initialize all animations
    initializeAllAnimations() {
        // Add additional CSS animations
        const additionalStyles = `
            @keyframes buttonHover {
                0% { transform: translateY(0); }
                50% { transform: translateY(-3px); }
                100% { transform: translateY(-3px); }
            }
            
            @keyframes overlayReveal {
                from { opacity: 0; transform: scale(1.1); }
                to { opacity: 1; transform: scale(1); }
            }
            
            @keyframes liquidMorph {
                0% { border-radius: 20px; }
                50% { border-radius: 50px 20px; }
                100% { border-radius: 20px; }
            }
            
            .service-card:hover {
                animation: liquidMorph 2s ease-in-out infinite;
            }
            
            .team-member:hover .member-avatar {
                animation: avatarFloat 1s ease-in-out infinite;
            }
            
            @keyframes avatarFloat {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-5px); }
            }
            
            .portfolio-card:hover .portfolio-image {
                animation: imageShift 0.5s ease forwards;
            }
            
            @keyframes imageShift {
                from { transform: scale(1); }
                to { transform: scale(1.05); }
            }
        `;
        
        const styleSheet = document.createElement('style');
        styleSheet.textContent = additionalStyles;
        document.head.appendChild(styleSheet);
    }
}

// Initialize the website when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SkyLineWebsite();
});

// Additional utility functions for enhanced interactions
function createRippleEffect(event) {
    const button = event.currentTarget;
    const circle = document.createElement('span');
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;

    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${event.clientX - button.offsetLeft - radius}px`;
    circle.style.top = `${event.clientY - button.offsetTop - radius}px`;
    circle.classList.add('ripple');

    const ripple = button.querySelector('.ripple');
    if (ripple) {
        ripple.remove();
    }

    button.appendChild(circle);
}

// Add ripple effect to buttons
document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', createRippleEffect);
    });
});

// Performance optimization: Debounce scroll events
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Apply debouncing to scroll events
window.addEventListener('scroll', debounce(() => {
    // Optimized scroll handling
}, 16)); // ~60fps

// Add CSS for ripple effect
const rippleCSS = `
.ripple {
    position: absolute;
    border-radius: 50%;
    transform: scale(0);
    animation: ripple-animation 0.6s linear;
    background-color: rgba(255, 255, 255, 0.7);
}

@keyframes ripple-animation {
    to {
        transform: scale(4);
        opacity: 0;
    }
}

.btn {
    position: relative;
    overflow: hidden;
}
`;

const rippleStyle = document.createElement('style');
rippleStyle.textContent = rippleCSS;
document.head.appendChild(rippleStyle);