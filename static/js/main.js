// static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add loading state to forms - FIXED VERSION
    const forms = document.querySelectorAll('form:not(.no-loading)');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Skip if form has no-loading class
            if (form.classList.contains('no-loading')) return;
            
            // Skip if it's a delete form or logout form
            if (form.id && (form.id.includes('delete') || form.id.includes('logout'))) return;
            
            const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
            if (!submitBtn) return;
            
            // Check if form is valid before showing loading
            if (form.checkValidity && !form.checkValidity()) {
                return; // Let browser handle validation
            }
            
            // Store original button content
            const originalContent = submitBtn.innerHTML;
            
            // Add loading state
            submitBtn.disabled = true;
            if (submitBtn.tagName === 'BUTTON') {
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
            } else {
                submitBtn.value = 'Loading...';
            }
            
            // Reset button after 10 seconds (failsafe)
            setTimeout(() => {
                submitBtn.disabled = false;
                if (submitBtn.tagName === 'BUTTON') {
                    submitBtn.innerHTML = originalContent;
                } else {
                    submitBtn.value = originalContent;
                }
            }, 10000);
        });
    });

    // Mobile menu active state
    const currentPath = window.location.pathname;
    const mobileNavItems = document.querySelectorAll('.mobile-nav-item');
    mobileNavItems.forEach(item => {
        if (item.getAttribute('href') === currentPath) {
            item.classList.add('active');
        }
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
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

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Dynamic form validation feedback
    const validateForms = document.querySelectorAll('.needs-validation');
    validateForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Time slot selection for booking form
    const timeSlots = document.querySelectorAll('.time-slot');
    timeSlots.forEach(slot => {
        slot.addEventListener('click', function() {
            // Remove active class from all slots
            timeSlots.forEach(s => s.classList.remove('active'));
            // Add active class to clicked slot
            this.classList.add('active');
            // Update hidden input if exists
            const timeInput = document.getElementById('selected-time');
            if (timeInput) {
                timeInput.value = this.dataset.time;
            }
        });
    });

    // Barber card hover effects
    const barberCards = document.querySelectorAll('.barber-card');
    barberCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Image preview for file inputs
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            const previewId = this.dataset.preview;
            if (file && previewId) {
                const preview = document.getElementById(previewId);
                if (preview) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        preview.src = e.target.result;
                        preview.style.display = 'block';
                    };
                    reader.readAsDataURL(file);
                }
            }
        });
    });

    // Rating stars interaction
    const ratingContainers = document.querySelectorAll('.rating-input');
    ratingContainers.forEach(container => {
        const stars = container.querySelectorAll('.star');
        const input = container.querySelector('input[type="hidden"]');
        
        stars.forEach((star, index) => {
            star.addEventListener('click', function() {
                const rating = index + 1;
                input.value = rating;
                
                // Update star display
                stars.forEach((s, i) => {
                    if (i < rating) {
                        s.classList.add('active');
                    } else {
                        s.classList.remove('active');
                    }
                });
            });
            
            star.addEventListener('mouseenter', function() {
                const hoverRating = index + 1;
                stars.forEach((s, i) => {
                    if (i < hoverRating) {
                        s.classList.add('hover');
                    } else {
                        s.classList.remove('hover');
                    }
                });
            });
        });
        
        container.addEventListener('mouseleave', function() {
            stars.forEach(s => s.classList.remove('hover'));
        });
    });
});