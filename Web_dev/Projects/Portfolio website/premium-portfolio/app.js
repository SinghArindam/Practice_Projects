// Global variables
let scene, camera, renderer, particles, particleSystem;
let mouseX = 0, mouseY = 0;
let windowHalfX = window.innerWidth / 2;
let windowHalfY = window.innerHeight / 2;
let isLoaded = false;
let threeJSLoaded = false;

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing...');
    initLoading();
    checkThreeJS();
    initTypewriter();
    initNavigation();
    initScrollAnimations();
    initFormHandling();
    initParticleInteractions();
    
    // Force hide loading screen after maximum time
    setTimeout(() => {
        console.log('Force hiding loading screen');
        hideLoadingScreen();
    }, 4000);
});

// Check if Three.js is loaded and initialize
function checkThreeJS() {
    if (typeof THREE !== 'undefined') {
        console.log('Three.js loaded, initializing particle system...');
        threeJSLoaded = true;
        initThreeJS();
    } else {
        console.log('Three.js not loaded yet, retrying...');
        setTimeout(checkThreeJS, 100);
    }
}

// Loading Screen
function initLoading() {
    console.log('Initializing loading screen...');
    const progressBar = document.querySelector('.progress-bar');
    let progress = 0;
    
    const loadingInterval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress >= 100) {
            progress = 100;
            clearInterval(loadingInterval);
            setTimeout(() => {
                hideLoadingScreen();
            }, 1000);
        }
        if (progressBar) {
            progressBar.style.width = progress + '%';
        }
    }, 200);
}

function hideLoadingScreen() {
    console.log('Hiding loading screen...');
    const loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
        loadingScreen.style.opacity = '0';
        setTimeout(() => {
            loadingScreen.style.display = 'none';
            isLoaded = true;
            startAnimations();
            console.log('Loading screen hidden, starting animations...');
        }, 500);
    }
}

// Three.js Particle System
function initThreeJS() {
    try {
        const canvas = document.getElementById('particle-canvas');
        if (!canvas) {
            console.error('Canvas not found');
            return;
        }
        
        console.log('Initializing Three.js...');
        
        // Scene setup
        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setClearColor(0x000000, 0);
        
        // Create particle system
        createParticleSystem();
        
        // Position camera
        camera.position.z = 50;
        
        // Start animation loop
        animate();
        
        // Handle window resize
        window.addEventListener('resize', onWindowResize);
        
        // Mouse movement tracking
        document.addEventListener('mousemove', onDocumentMouseMove);
        
        console.log('Three.js initialized successfully');
    } catch (error) {
        console.error('Error initializing Three.js:', error);
        // Continue without Three.js if it fails
        createFallbackBackground();
    }
}

function createFallbackBackground() {
    console.log('Creating fallback background...');
    const canvas = document.getElementById('particle-canvas');
    if (canvas) {
        canvas.style.background = `
            radial-gradient(circle at 20% 50%, rgba(0, 0, 255, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 215, 0, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(255, 0, 0, 0.2) 0%, transparent 50%),
            linear-gradient(135deg, #000000 0%, #0D0D0D 100%)
        `;
        canvas.style.animation = 'fallbackFloat 10s ease-in-out infinite alternate';
    }
    
    // Add fallback animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fallbackFloat {
            0% { transform: scale(1) rotate(0deg); }
            100% { transform: scale(1.05) rotate(2deg); }
        }
    `;
    document.head.appendChild(style);
}

function createParticleSystem() {
    try {
        const particleCount = 1500; // Reduced for better performance
        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        const velocities = new Float32Array(particleCount * 3);
        const colors = new Float32Array(particleCount * 3);
        
        // Create sphere of particles
        for (let i = 0; i < particleCount; i++) {
            const i3 = i * 3;
            
            // Spherical distribution
            const radius = 15 + Math.random() * 15;
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.random() * Math.PI;
            
            positions[i3] = radius * Math.sin(phi) * Math.cos(theta);
            positions[i3 + 1] = radius * Math.sin(phi) * Math.sin(theta);
            positions[i3 + 2] = radius * Math.cos(phi);
            
            // Random velocities
            velocities[i3] = (Math.random() - 0.5) * 0.01;
            velocities[i3 + 1] = (Math.random() - 0.5) * 0.01;
            velocities[i3 + 2] = (Math.random() - 0.5) * 0.01;
            
            // Color variations (golden to blue)
            const colorChoice = Math.random();
            if (colorChoice < 0.6) {
                // Golden
                colors[i3] = 1.0;
                colors[i3 + 1] = 0.84;
                colors[i3 + 2] = 0.0;
            } else if (colorChoice < 0.8) {
                // Blue
                colors[i3] = 0.0;
                colors[i3 + 1] = 0.0;
                colors[i3 + 2] = 1.0;
            } else {
                // White
                colors[i3] = 1.0;
                colors[i3 + 1] = 1.0;
                colors[i3 + 2] = 1.0;
            }
        }
        
        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('velocity', new THREE.BufferAttribute(velocities, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        
        // Particle material
        const material = new THREE.PointsMaterial({
            size: 0.8,
            vertexColors: true,
            transparent: true,
            opacity: 0.8,
            blending: THREE.AdditiveBlending
        });
        
        particleSystem = new THREE.Points(geometry, material);
        scene.add(particleSystem);
        
        // Store reference to positions and velocities
        particles = {
            positions: positions,
            velocities: velocities,
            geometry: geometry
        };
        
        console.log('Particle system created successfully');
    } catch (error) {
        console.error('Error creating particle system:', error);
    }
}

function animate() {
    if (!threeJSLoaded || !renderer || !scene || !camera) return;
    
    requestAnimationFrame(animate);
    
    try {
        if (particleSystem && isLoaded) {
            // Rotate particle system
            particleSystem.rotation.y += 0.003;
            particleSystem.rotation.x += 0.001;
            
            // Update particle positions
            if (particles && particles.positions && particles.velocities) {
                const positions = particles.positions;
                const velocities = particles.velocities;
                
                for (let i = 0; i < positions.length; i += 3) {
                    // Apply mouse influence
                    const mouseInfluence = 0.00005;
                    velocities[i] += (mouseX - windowHalfX) * mouseInfluence;
                    velocities[i + 1] += -(mouseY - windowHalfY) * mouseInfluence;
                    
                    // Update positions
                    positions[i] += velocities[i];
                    positions[i + 1] += velocities[i + 1];
                    positions[i + 2] += velocities[i + 2];
                    
                    // Boundary constraints (sphere)
                    const distance = Math.sqrt(
                        positions[i] * positions[i] +
                        positions[i + 1] * positions[i + 1] +
                        positions[i + 2] * positions[i + 2]
                    );
                    
                    if (distance > 30) {
                        const factor = 30 / distance;
                        positions[i] *= factor;
                        positions[i + 1] *= factor;
                        positions[i + 2] *= factor;
                        
                        // Bounce back
                        velocities[i] *= -0.3;
                        velocities[i + 1] *= -0.3;
                        velocities[i + 2] *= -0.3;
                    }
                    
                    // Damping
                    velocities[i] *= 0.995;
                    velocities[i + 1] *= 0.995;
                    velocities[i + 2] *= 0.995;
                }
                
                particles.geometry.attributes.position.needsUpdate = true;
            }
        }
        
        renderer.render(scene, camera);
    } catch (error) {
        console.error('Animation error:', error);
    }
}

function onWindowResize() {
    windowHalfX = window.innerWidth / 2;
    windowHalfY = window.innerHeight / 2;
    
    if (camera && renderer) {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    }
}

function onDocumentMouseMove(event) {
    mouseX = event.clientX;
    mouseY = event.clientY;
}

// Typewriter Effect
function initTypewriter() {
    console.log('Initializing typewriter effect...');
    const typewriterElement = document.getElementById('typewriter');
    const text = 'ALEX PORTFOLIO';
    let i = 0;
    
    function typeWriter() {
        if (i < text.length && typewriterElement) {
            typewriterElement.innerHTML += text.charAt(i);
            i++;
            const delay = Math.random() * 100 + 50; // Variable typing speed
            setTimeout(typeWriter, delay);
        }
    }
    
    // Start typewriter effect after loading
    setTimeout(() => {
        if (isLoaded) {
            typeWriter();
        } else {
            // Start anyway after a delay
            setTimeout(typeWriter, 2000);
        }
    }, 1500);
}

// Navigation
function initNavigation() {
    console.log('Initializing navigation...');
    const nav = document.getElementById('nav');
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Scroll effect
    window.addEventListener('scroll', () => {
        if (nav) {
            if (window.scrollY > 100) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }
        }
    });
    
    // Mobile menu toggle
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
        });
    }
    
    // Close mobile menu when clicking links
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (navMenu && navToggle) {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            }
        });
    });
    
    // Active link highlighting
    window.addEventListener('scroll', () => {
        let current = '';
        const sections = document.querySelectorAll('section');
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (scrollY >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + current) {
                link.classList.add('active');
            }
        });
    });
}

// Scroll Animations
function initScrollAnimations() {
    console.log('Initializing scroll animations...');
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                
                // Trigger specific animations
                if (entry.target.classList.contains('skills')) {
                    animateSkills();
                }
                if (entry.target.classList.contains('about')) {
                    animateStats();
                }
            }
        });
    }, observerOptions);
    
    // Observe sections
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        observer.observe(section);
    });
    
    // Add CSS for animations
    addAnimationStyles();
}

function addAnimationStyles() {
    const style = document.createElement('style');
    style.textContent = `
        section {
            opacity: 0;
            transform: translateY(30px);
            transition: all 0.8s cubic-bezier(0.25, 0.8, 0.25, 1);
        }
        
        section.animate-in {
            opacity: 1;
            transform: translateY(0);
        }
        
        .glass-card {
            opacity: 0;
            transform: translateY(30px);
            transition: all 0.6s cubic-bezier(0.25, 0.8, 0.25, 1);
        }
        
        .animate-in .glass-card {
            opacity: 1;
            transform: translateY(0);
        }
        
        .project-card:nth-child(1) { transition-delay: 0.1s; }
        .project-card:nth-child(2) { transition-delay: 0.2s; }
        .project-card:nth-child(3) { transition-delay: 0.3s; }
        
        .hero {
            opacity: 1 !important;
            transform: none !important;
        }
    `;
    document.head.appendChild(style);
}

// Skills Animation
function animateSkills() {
    console.log('Animating skills...');
    const skillItems = document.querySelectorAll('.skill-item');
    
    skillItems.forEach((item, index) => {
        setTimeout(() => {
            const progress = item.querySelector('.skill-progress');
            const percentage = item.getAttribute('data-skill');
            if (progress) {
                progress.style.width = percentage + '%';
            }
        }, index * 200);
    });
}

// Stats Counter Animation
function animateStats() {
    console.log('Animating stats...');
    const statNumbers = document.querySelectorAll('.stat-number');
    
    statNumbers.forEach(stat => {
        const target = parseInt(stat.getAttribute('data-target'));
        const increment = target / 100;
        let current = 0;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            stat.textContent = Math.floor(current) + (target === 100 ? '%' : '+');
        }, 20);
    });
}

// Form Handling
function initFormHandling() {
    console.log('Initializing form handling...');
    const form = document.getElementById('contact-form');
    
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            console.log('Form submitted');
            
            // Get form data
            const formData = new FormData(form);
            const data = {
                name: formData.get('name'),
                email: formData.get('email'),
                subject: formData.get('subject'),
                message: formData.get('message')
            };
            
            console.log('Form data:', data);
            
            // Simulate form submission
            const submitButton = form.querySelector('button[type="submit"]');
            const originalText = submitButton.querySelector('span').textContent;
            
            submitButton.querySelector('span').textContent = 'Sending...';
            submitButton.disabled = true;
            
            setTimeout(() => {
                submitButton.querySelector('span').textContent = 'Message Sent!';
                createSuccessParticles(submitButton);
                setTimeout(() => {
                    submitButton.querySelector('span').textContent = originalText;
                    submitButton.disabled = false;
                    form.reset();
                }, 2000);
            }, 1500);
        });
        
        // Form validation
        const inputs = form.querySelectorAll('.form-control');
        inputs.forEach(input => {
            input.addEventListener('blur', validateField);
            input.addEventListener('input', clearValidation);
        });
    }
}

function validateField(e) {
    const field = e.target;
    const value = field.value.trim();
    
    // Remove existing validation
    clearValidation(e);
    
    if (!value) {
        showValidationError(field, 'This field is required');
        return;
    }
    
    if (field.type === 'email' && !isValidEmail(value)) {
        showValidationError(field, 'Please enter a valid email');
        return;
    }
    
    showValidationSuccess(field);
}

function clearValidation(e) {
    const field = e.target;
    const group = field.parentNode;
    group.classList.remove('error', 'success');
    
    const existingMessage = group.querySelector('.validation-message');
    if (existingMessage) {
        existingMessage.remove();
    }
}

function showValidationError(field, message) {
    const group = field.parentNode;
    group.classList.add('error');
    
    const messageEl = document.createElement('div');
    messageEl.className = 'validation-message error-message';
    messageEl.textContent = message;
    group.appendChild(messageEl);
}

function showValidationSuccess(field) {
    const group = field.parentNode;
    group.classList.add('success');
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Particle Interactions
function initParticleInteractions() {
    console.log('Initializing particle interactions...');
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('mouseenter', () => {
            createButtonParticles(button);
        });
        
        button.addEventListener('click', (e) => {
            createClickParticles(e);
        });
    });
}

function createButtonParticles(button) {
    const particleContainer = button.querySelector('.btn-particles');
    if (!particleContainer) return;
    
    for (let i = 0; i < 6; i++) {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: absolute;
            width: 4px;
            height: 4px;
            background: #FFD700;
            border-radius: 50%;
            pointer-events: none;
            animation: buttonParticle 0.6s ease-out forwards;
        `;
        
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        
        particleContainer.appendChild(particle);
        
        setTimeout(() => {
            if (particle.parentNode) {
                particle.remove();
            }
        }, 600);
    }
}

function createClickParticles(e) {
    const rect = e.target.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    for (let i = 0; i < 8; i++) {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: fixed;
            left: ${rect.left + x}px;
            top: ${rect.top + y}px;
            width: 6px;
            height: 6px;
            background: #FFD700;
            border-radius: 50%;
            pointer-events: none;
            z-index: 10000;
            animation: clickParticle 0.8s ease-out forwards;
        `;
        
        const angle = (i / 8) * Math.PI * 2;
        const distance = 50 + Math.random() * 30;
        const endX = Math.cos(angle) * distance;
        const endY = Math.sin(angle) * distance;
        
        particle.style.setProperty('--endX', endX + 'px');
        particle.style.setProperty('--endY', endY + 'px');
        
        document.body.appendChild(particle);
        
        setTimeout(() => {
            if (particle.parentNode) {
                particle.remove();
            }
        }, 800);
    }
}

function createSuccessParticles(element) {
    const rect = element.getBoundingClientRect();
    
    for (let i = 0; i < 15; i++) {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: fixed;
            left: ${rect.left + rect.width / 2}px;
            top: ${rect.top + rect.height / 2}px;
            width: 8px;
            height: 8px;
            background: #00FF00;
            border-radius: 50%;
            pointer-events: none;
            z-index: 10000;
            animation: successParticle 1s ease-out forwards;
        `;
        
        const angle = (i / 15) * Math.PI * 2;
        const velocity = 40 + Math.random() * 40;
        const endX = Math.cos(angle) * velocity;
        const endY = Math.sin(angle) * velocity;
        
        particle.style.setProperty('--endX', endX + 'px');
        particle.style.setProperty('--endY', endY + 'px');
        
        document.body.appendChild(particle);
        
        setTimeout(() => {
            if (particle.parentNode) {
                particle.remove();
            }
        }, 1000);
    }
}

// Start animations
function startAnimations() {
    console.log('Starting animations...');
    // Add animation keyframes
    const animationStyles = document.createElement('style');
    animationStyles.textContent = `
        @keyframes buttonParticle {
            0% {
                transform: scale(0);
                opacity: 1;
            }
            100% {
                transform: scale(1) translate(${Math.random() * 40 - 20}px, ${Math.random() * 40 - 20}px);
                opacity: 0;
            }
        }
        
        @keyframes clickParticle {
            0% {
                transform: scale(0);
                opacity: 1;
            }
            100% {
                transform: scale(1) translate(var(--endX), var(--endY));
                opacity: 0;
            }
        }
        
        @keyframes successParticle {
            0% {
                transform: scale(0);
                opacity: 1;
            }
            100% {
                transform: scale(1) translate(var(--endX), var(--endY));
                opacity: 0;
            }
        }
        
        .form-group.error .form-control {
            border-color: #FF0000;
            box-shadow: 0 0 0 3px rgba(255, 0, 0, 0.2);
        }
        
        .form-group.success .form-control {
            border-color: #00FF00;
            box-shadow: 0 0 0 3px rgba(0, 255, 0, 0.2);
        }
        
        .validation-message {
            position: absolute;
            bottom: -20px;
            left: 15px;
            font-size: 12px;
            font-weight: 500;
        }
        
        .error-message {
            color: #FF0000;
        }
    `;
    document.head.appendChild(animationStyles);
    
    // Trigger initial animations
    setTimeout(() => {
        const heroSection = document.querySelector('.hero');
        if (heroSection) {
            heroSection.classList.add('animate-in');
        }
    }, 500);
}

// Smooth scrolling for navigation links
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Performance optimization
let ticking = false;

function updateAnimations() {
    if (!ticking) {
        requestAnimationFrame(() => {
            ticking = false;
        });
        ticking = true;
    }
}

window.addEventListener('scroll', updateAnimations);

// Preload critical resources
window.addEventListener('load', () => {
    console.log('Window loaded');
    document.body.classList.add('loaded');
    
    // Ensure loading screen is hidden
    if (!isLoaded) {
        hideLoadingScreen();
    }
});