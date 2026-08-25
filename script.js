// ============================================
// MALERFIRMAET HANS LARSEN — SCRIPT
// ============================================

(function() {
  'use strict';

  // ===== Mobile menu toggle =====
  const menuToggle = document.getElementById('menuToggle');
  const navMenu = document.getElementById('navMenu');

  if (menuToggle && navMenu) {
    menuToggle.addEventListener('click', function(e) {
      e.stopPropagation();
      const isOpen = navMenu.classList.toggle('open');
      menuToggle.classList.toggle('active', isOpen);
      menuToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    // Close menu when clicking a link
    navMenu.querySelectorAll('a').forEach(function(a) {
      a.addEventListener('click', function() {
        navMenu.classList.remove('open');
        menuToggle.classList.remove('active');
        menuToggle.setAttribute('aria-expanded', 'false');
      });
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
      if (!navMenu.contains(e.target) && !menuToggle.contains(e.target)) {
        navMenu.classList.remove('open');
        menuToggle.classList.remove('active');
        menuToggle.setAttribute('aria-expanded', 'false');
      }
    });

    // Close menu on Escape
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && navMenu.classList.contains('open')) {
        navMenu.classList.remove('open');
        menuToggle.classList.remove('active');
        menuToggle.setAttribute('aria-expanded', 'false');
        menuToggle.focus();
      }
    });
  }

  // ===== Sticky nav shrink on scroll =====
  const nav = document.querySelector('nav');
  if (nav) {
    function handleNavScroll() {
      nav.classList.toggle('scrolled', window.pageYOffset > 20);
    }
    window.addEventListener('scroll', handleNavScroll, { passive: true });
    handleNavScroll();
  }

  // ===== Scroll reveal animations =====
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-stagger').forEach(function(el) {
      observer.observe(el);
    });
  } else {
    // Fallback: just show everything
    document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-stagger').forEach(function(el) {
      el.classList.add('visible');
    });
  }

  // ===== Form submit handler =====
  const form = document.getElementById('contactForm');
  if (form) {
    const formContent = document.getElementById('formContent');
    const formSuccess = document.getElementById('formSuccess');

    form.addEventListener('submit', function(e) {
      e.preventDefault();
      // In production, replace with real backend (e.g. Formspree, Web3Forms, or own server)
      // Example for Formspree:
      // fetch('https://formspree.io/f/YOUR_ID', {
      //   method: 'POST',
      //   body: new FormData(form),
      //   headers: { Accept: 'application/json' }
      // }).then(...)
      
      if (formContent) formContent.style.display = 'none';
      if (formSuccess) formSuccess.classList.add('active');
      
      // Scroll to success message
      if (formSuccess) {
        formSuccess.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });
  }

  // ===== Smooth scroll for in-page anchors =====
  document.querySelectorAll('a[href^="#"]').forEach(function(link) {
    link.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href === '#' || href.length < 2) return;
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        const offset = 80;
        const targetPos = target.getBoundingClientRect().top + window.pageYOffset - offset;
        window.scrollTo({ top: targetPos, behavior: 'smooth' });
      }
    });
  });

})();
