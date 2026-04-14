// ========================
// 1. Theme Toggle (Dark/Light Mode)
// ========================
const themeToggle = document.getElementById('themeToggle');
const html = document.documentElement;

function setTheme(theme) {
  if (theme === 'dark') {
    html.classList.add('dark');
    localStorage.setItem('theme', 'dark');
  } else {
    html.classList.remove('dark');
    localStorage.setItem('theme', 'light');
  }
  updateThemeIcon();
}

function updateThemeIcon() {
  if (!themeToggle) return;
  const isDark = html.classList.contains('dark');
  const icon = themeToggle.querySelector('i');
  if (icon) {
    icon.className = isDark ? 'fas fa-sun text-lg' : 'fas fa-moon text-lg';
  }
}

const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
  setTheme(savedTheme);
} else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
  setTheme('dark');
} else {
  setTheme('light');
}

if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    const newTheme = html.classList.contains('dark') ? 'light' : 'dark';
    setTheme(newTheme);
  });
}

// ========================
// 2. Mobile Menu Toggle
// ========================
const mobileToggle = document.getElementById('mobileMenuToggle');
const mobileMenu = document.getElementById('mobileMenu');

if (mobileToggle && mobileMenu) {
  mobileToggle.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
    const expanded = mobileMenu.classList.contains('hidden') ? 'false' : 'true';
    mobileToggle.setAttribute('aria-expanded', expanded);
  });
}

// ========================
// 3. Profile Dropdown
// ========================
const profileBtn = document.getElementById('profileBtn');
const profileDropdown = document.getElementById('profileDropdown');

if (profileBtn && profileDropdown) {
  profileBtn.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    profileDropdown.classList.toggle('hidden');
  });

  document.addEventListener('click', (e) => {
    if (!profileBtn.contains(e.target) && !profileDropdown.contains(e.target)) {
      profileDropdown.classList.add('hidden');
    }
  });
}

// ========================
// 4. Toast Notifications
// ========================
const toastContainer = document.getElementById('toastContainer');

window.showToast = function(message, type = 'info') {
  if (!toastContainer) return;
  const toast = document.createElement('div');
  const bgColor = {
    info: 'bg-indigo-500',
    success: 'bg-emerald-500',
    warning: 'bg-amber-500',
    error: 'bg-rose-500',
    danger: 'bg-rose-500'
  }[type] || 'bg-indigo-500';

  toast.className = `flex items-center justify-between gap-3 rounded-lg px-4 py-3 text-white shadow-lg transition-all duration-300 transform translate-x-full`;
  toast.style.backgroundColor = bgColor;
  toast.innerHTML = `
    <div class="flex-1 text-sm">${message}</div>
    <button class="rounded-full p-1 hover:bg-white/20 transition">✕</button>
  `;
  toastContainer.appendChild(toast);
  
  setTimeout(() => toast.classList.remove('translate-x-full'), 10);
  
  toast.querySelector('button').addEventListener('click', () => {
    toast.classList.add('translate-x-full');
    setTimeout(() => toast.remove(), 300);
  });
  
  setTimeout(() => {
    if (toast.parentNode) {
      toast.classList.add('translate-x-full');
      setTimeout(() => toast.remove(), 300);
    }
  }, 4000);
};

// Flash messages from Flask
document.addEventListener('DOMContentLoaded', () => {
  const flashMessages = document.querySelectorAll('[data-flash]');
  flashMessages.forEach(msg => {
    showToast(msg.dataset.message, msg.dataset.category);
  });
});

// ========================
// 5. Scroll Animations
// ========================
const animatedElements = document.querySelectorAll(
  '.group, .feature-item, [class*="rounded-2xl"], [class*="rounded-3xl"], .grid > div'
);

function isInViewport(el) {
  const rect = el.getBoundingClientRect();
  const buffer = 100;
  return rect.top < window.innerHeight - buffer && rect.bottom > 0;
}

function animateVisibleElements() {
  animatedElements.forEach(el => {
    if (isInViewport(el) && !el.classList.contains('animated')) {
      el.classList.add('animate-fade-up', 'animated');
    }
  });
}

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
      entry.target.classList.add('animate-fade-up', 'animated');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -30px 0px' });

animatedElements.forEach(el => {
  observer.observe(el);
});

window.addEventListener('load', () => {
  setTimeout(animateVisibleElements, 100);
});
window.addEventListener('scroll', animateVisibleElements);
animateVisibleElements();

// ========================
// 6. Cursor-Follow Glow
// ========================
const glow = document.createElement('div');
glow.className = 'pointer-events-none fixed top-0 left-0 w-96 h-96 rounded-full bg-indigo-500/5 dark:bg-indigo-400/5 blur-3xl transition-all duration-300 ease-out z-0';
document.body.appendChild(glow);

document.addEventListener('mousemove', (e) => {
  glow.style.transform = `translate(${e.clientX - 192}px, ${e.clientY - 192}px)`;
});

// ========================
// 7. Enhanced Active Navigation Highlight (Client-Side) – FIXED
// ========================
function setActiveNavLink() {
  // Normalize current path: remove trailing slash, ensure it starts with /
  let currentPath = window.location.pathname;
  if (currentPath !== '/' && currentPath.endsWith('/')) {
    currentPath = currentPath.slice(0, -1);
  }
  
  // Select all possible navigation links (desktop + mobile + any dropdown)
  const navLinks = document.querySelectorAll(
    'nav a[href], #mobileMenu a[href], .dropdown-menu a[href]'
  );
  
  // First, remove any existing active classes
  navLinks.forEach(link => {
    link.classList.remove('text-indigo-600', 'dark:text-indigo-400', 'font-semibold', 'active-route');
    // Also remove from parent <li> if you have custom styles
    const parentLi = link.closest('li');
    if (parentLi) parentLi.classList.remove('active');
  });
  
  navLinks.forEach(link => {
    let href = link.getAttribute('href');
    if (!href || href === '#' || href.startsWith('http') || href.startsWith('https')) return;
    
    // Normalize href: remove trailing slash, ensure it starts with /
    if (href !== '/' && href.endsWith('/')) {
      href = href.slice(0, -1);
    }
    
    // Debug: log to console (remove in production)
    // console.log('Checking link:', href, 'against', currentPath);
    
    // Exact match
    if (href === currentPath) {
      link.classList.add('text-indigo-600', 'dark:text-indigo-400', 'font-semibold', 'active-route');
      const parentLi = link.closest('li');
      if (parentLi) parentLi.classList.add('active');
    }
    // Parent route match (e.g., '/dashboard' for '/dashboard/settings')
    else if (href !== '/' && currentPath.startsWith(href + '/')) {
      link.classList.add('text-indigo-600', 'dark:text-indigo-400', 'font-semibold', 'active-route');
      const parentLi = link.closest('li');
      if (parentLi) parentLi.classList.add('active');
    }
    // Home page special case
    else if (href === '/' && currentPath === '/') {
      link.classList.add('text-indigo-600', 'dark:text-indigo-400', 'font-semibold', 'active-route');
      const parentLi = link.closest('li');
      if (parentLi) parentLi.classList.add('active');
    }
  });
}

// Run after DOM is fully loaded
document.addEventListener('DOMContentLoaded', setActiveNavLink);
// Also run on popstate (browser back/forward)
window.addEventListener('popstate', setActiveNavLink);
// Optional: run on hashchange if you use anchor links
window.addEventListener('hashchange', setActiveNavLink);

// ========================
// 8. Matrix Background Effect
// ========================
function initMatrixBackground() {
  const canvas = document.getElementById('matrixBg');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  let width, height, columns, drops, fontSize, chars;
  
  function resize() {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;
    fontSize = 12;
    columns = Math.floor(width / fontSize);
    drops = [];
    for (let i = 0; i < columns; i++) drops[i] = 1;
    chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン";
  }
  
  function draw() {
    ctx.fillStyle = "rgba(10, 10, 10, 0.04)";
    ctx.fillRect(0, 0, width, height);
    ctx.fillStyle = "#00ff41";
    ctx.font = `${fontSize}px 'JetBrains Mono', monospace`;
    for (let i = 0; i < drops.length; i++) {
      const text = chars[Math.floor(Math.random() * chars.length)];
      const opacity = Math.random() * 0.5 + 0.3;
      ctx.fillStyle = `rgba(0, 255, 65, ${opacity})`;
      ctx.fillText(text, i * fontSize, drops[i] * fontSize);
      if (drops[i] * fontSize > height && Math.random() > 0.975) {
        drops[i] = 0;
      }
      drops[i]++;
    }
  }
  
  resize();
  window.addEventListener('resize', resize);
  setInterval(draw, 35);
}

// ========================
// 9. API Documentation Functions
// ========================
function initApiDocs() {
  const tabButtons = document.querySelectorAll('.tab-btn-api');
  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const parent = btn.closest('section');
      const target = btn.dataset.tab;
      parent.querySelectorAll('.tab-btn-api').forEach(b => {
        b.classList.remove('bg-indigo-600', 'text-white');
        b.classList.add('bg-slate-200', 'dark:bg-slate-700', 'text-slate-700', 'dark:text-slate-300');
      });
      btn.classList.remove('bg-slate-200', 'dark:bg-slate-700', 'text-slate-700', 'dark:text-slate-300');
      btn.classList.add('bg-indigo-600', 'text-white');
      parent.querySelectorAll('.code-block-api').forEach(block => block.classList.add('hidden'));
      const targetBlock = parent.querySelector(`[data-code="${target}"]`);
      if (targetBlock) targetBlock.classList.remove('hidden');
    });
  });

  document.querySelectorAll('.copy-btn-api').forEach(btn => {
    btn.addEventListener('click', async () => {
      const targetId = btn.dataset.copyTarget;
      const codeElement = document.getElementById(targetId);
      if (codeElement) {
        const text = codeElement.innerText;
        await navigator.clipboard.writeText(text);
        const original = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-check"></i> Copied!';
        setTimeout(() => btn.innerHTML = original, 2000);
      }
    });
  });

  const searchInput = document.getElementById('searchInput');
  const navLinks = document.querySelectorAll('.nav-link-api');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      const term = e.target.value.toLowerCase();
      navLinks.forEach(link => {
        const text = link.textContent.toLowerCase();
        link.style.display = text.includes(term) ? 'block' : 'none';
      });
    });
  }

  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        history.pushState(null, null, this.getAttribute('href'));
      }
    });
  });

  const sections = document.querySelectorAll('section[id]');
  window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(section => {
      const sectionTop = section.offsetTop - 100;
      if (pageYOffset >= sectionTop) current = section.getAttribute('id');
    });
    navLinks.forEach(link => {
      link.classList.remove('text-indigo-600', 'dark:text-indigo-400', 'font-semibold');
      if (link.getAttribute('href') === `#${current}`) {
        link.classList.add('text-indigo-600', 'dark:text-indigo-400', 'font-semibold');
      }
    });
  });
}

// ========================
// 10. Login / Register Page Enhancements
// ========================
function initAuthPages() {
  const passwordInput = document.getElementById('regPassword');
  const strengthHint = document.getElementById('passwordStrengthHint');
  if (passwordInput && strengthHint) {
    passwordInput.addEventListener('input', () => {
      const val = passwordInput.value;
      let strength = '';
      if (val.length === 0) strength = '';
      else if (val.length < 6) strength = '❌ Too short (min 6 characters)';
      else if (!/[0-9]/.test(val)) strength = '⚠️ Add a number';
      else if (!/[!@#$%^&*]/.test(val)) strength = '⚠️ Add a special character (!@#$%^&*)';
      else strength = '✅ Strong password';
      strengthHint.textContent = strength;
      strengthHint.className = 'mt-1 text-xs ' + 
        (strength.includes('✅') ? 'text-green-600 dark:text-green-400' : 
         strength.includes('⚠️') ? 'text-amber-600 dark:text-amber-400' : 
         strength ? 'text-rose-600 dark:text-rose-400' : '');
    });
  }

  const confirmPassword = document.getElementById('regConfirmPassword');
  if (confirmPassword && passwordInput) {
    function checkMatch() {
      if (confirmPassword.value && confirmPassword.value !== passwordInput.value) {
        confirmPassword.setCustomValidity('Passwords do not match');
        confirmPassword.classList.add('border-rose-500', 'dark:border-rose-500');
      } else {
        confirmPassword.setCustomValidity('');
        confirmPassword.classList.remove('border-rose-500', 'dark:border-rose-500');
      }
    }
    passwordInput.addEventListener('input', checkMatch);
    confirmPassword.addEventListener('input', checkMatch);
  }

  const termsLink = document.getElementById('termsLink');
  const termsModal = document.getElementById('termsModal');
  const closeTermsModal = document.getElementById('closeTermsModal');
  const cancelTermsBtn = document.getElementById('cancelTermsBtn');
  const acceptTermsBtn = document.getElementById('acceptTermsBtn');
  const termsCheckbox = document.getElementById('termsCheckbox');
  const termsAgreeCheckbox = document.getElementById('termsAgreeCheckbox');
  const registerSubmitBtn = document.getElementById('registerSubmitBtn');

  if (termsLink && termsModal) {
    function openModal() {
      termsModal.classList.remove('hidden');
      termsModal.classList.add('flex');
    }
    function closeModal() {
      termsModal.classList.add('hidden');
      termsModal.classList.remove('flex');
    }
    termsLink.addEventListener('click', (e) => {
      e.preventDefault();
      openModal();
    });
    if (closeTermsModal) closeTermsModal.addEventListener('click', closeModal);
    if (cancelTermsBtn) cancelTermsBtn.addEventListener('click', closeModal);
    termsModal.addEventListener('click', (e) => {
      if (e.target === termsModal) closeModal();
    });
    if (acceptTermsBtn) {
      acceptTermsBtn.addEventListener('click', () => {
        if (termsAgreeCheckbox && termsAgreeCheckbox.checked) {
          if (termsCheckbox) termsCheckbox.checked = true;
          if (registerSubmitBtn) registerSubmitBtn.disabled = false;
          closeModal();
        } else {
          alert('Please agree to the terms by checking the box inside the modal.');
        }
      });
    }
    if (termsCheckbox) {
      termsCheckbox.addEventListener('change', () => {
        if (registerSubmitBtn) registerSubmitBtn.disabled = !termsCheckbox.checked;
      });
    }
    if (registerSubmitBtn) registerSubmitBtn.disabled = true;
  }

  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      const submitBtn = loginForm.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> AUTHENTICATING...';
      }
    });
  }

  const registerForm = document.getElementById('registerForm');
  if (registerForm) {
    registerForm.addEventListener('submit', (e) => {
      const submitBtn = registerForm.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> CREATING ACCOUNT...';
      }
    });
  }
}

// ========================
// 11. Initialize Everything
// ========================
document.addEventListener('DOMContentLoaded', () => {
  initMatrixBackground();
  if (document.querySelector('.tab-btn-api')) initApiDocs();
  initAuthPages();
});