// ========================
// Settings Page JavaScript
// ========================

document.addEventListener('DOMContentLoaded', function() {
  // ---------- Tab Switching ----------
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabPanes = document.querySelectorAll('.tab-pane');

  function activateTab(tabId) {
    tabPanes.forEach(pane => pane.classList.add('hidden'));
    const activePane = document.getElementById(`tab-${tabId}`);
    if (activePane) activePane.classList.remove('hidden');

    tabBtns.forEach(btn => {
      btn.classList.remove('text-indigo-600', 'dark:text-indigo-400', 'bg-slate-100', 'dark:bg-slate-800');
      if (btn.getAttribute('data-tab') === tabId) {
        btn.classList.add('text-indigo-600', 'dark:text-indigo-400', 'bg-slate-100', 'dark:bg-slate-800');
      }
    });
  }

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const tabId = btn.getAttribute('data-tab');
      activateTab(tabId);
    });
  });
  // Activate first tab (Logout) by default
  if (tabBtns.length) activateTab('Logout');

  // ---------- User Info: Password Strength & Match ----------
  const passwordInput = document.getElementById('password');
  const confirmInput = document.getElementById('confirm_password');
  const strengthBar = document.getElementById('passwordStrength');
  const lengthHint = document.getElementById('lengthHint');
  const numberHint = document.getElementById('numberHint');
  const specialHint = document.getElementById('specialHint');
  const matchFeedback = document.getElementById('passwordMatchFeedback');

  function checkPasswordStrength() {
    const val = passwordInput.value;
    let strength = 0;
    const lengthOk = val.length >= 8;
    const numberOk = /[0-9]/.test(val);
    const specialOk = /[!@#$%^&*]/.test(val);
    if (lengthOk) strength += 33;
    if (numberOk) strength += 33;
    if (specialOk) strength += 34;
    strengthBar.style.width = strength + '%';
    if (strength < 34) strengthBar.classList.replace('bg-rose-500', 'bg-rose-500');
    else if (strength < 67) strengthBar.classList.replace('bg-rose-500', 'bg-amber-500');
    else strengthBar.classList.replace('bg-amber-500', 'bg-emerald-500');
    lengthHint.className = lengthOk ? 'text-emerald-500' : 'text-slate-400';
    numberHint.className = numberOk ? 'text-emerald-500' : 'text-slate-400';
    specialHint.className = specialOk ? 'text-emerald-500' : 'text-slate-400';
    checkPasswordMatch();
  }

  function checkPasswordMatch() {
    if (confirmInput.value && passwordInput.value !== confirmInput.value) {
      matchFeedback.classList.remove('hidden');
      confirmInput.classList.add('border-rose-500');
    } else {
      matchFeedback.classList.add('hidden');
      confirmInput.classList.remove('border-rose-500');
    }
  }

  if (passwordInput) passwordInput.addEventListener('input', checkPasswordStrength);
  if (confirmInput) confirmInput.addEventListener('input', checkPasswordMatch);

  // User info form submission (prevent double submit)
  const userInfoForm = document.getElementById('userInfoForm');
  if (userInfoForm) {
    userInfoForm.addEventListener('submit', function(e) {
      const submitBtn = this.querySelector('button[type="submit"]');
      const spinner = document.getElementById('updateSpinner');
      if (submitBtn && spinner) {
        submitBtn.disabled = true;
        spinner.classList.remove('hidden');
      }
    });
  }

  // ---------- API Token Management ----------
  // Toggle token visibility
  document.querySelectorAll('.toggle-token-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      const id = this.getAttribute('data-id');
      const field = document.getElementById(`tokenField${id}`);
      const icon = document.getElementById(`toggleIcon${id}`);
      if (field.type === 'password') {
        field.type = 'text';
        icon.classList.replace('fa-eye', 'fa-eye-slash');
      } else {
        field.type = 'password';
        icon.classList.replace('fa-eye-slash', 'fa-eye');
      }
    });
  });

  // Copy token to clipboard
  document.querySelectorAll('.copy-token-btn').forEach(btn => {
    btn.addEventListener('click', async function() {
      const id = this.getAttribute('data-id');
      const field = document.getElementById(`tokenField${id}`);
      try {
        await navigator.clipboard.writeText(field.value);
        const original = this.innerHTML;
        this.innerHTML = '<i class="fas fa-check"></i> COPIED!';
        setTimeout(() => this.innerHTML = original, 1500);
      } catch (err) {
        alert('Failed to copy token');
      }
    });
  });

  // Delete token via AJAX
  document.querySelectorAll('.delete-token-form').forEach(form => {
    form.addEventListener('submit', async function(e) {
      e.preventDefault();
      const id = this.getAttribute('data-id');
      const url = this.getAttribute('data-url');
      if (confirm('Are you sure you want to delete this API token?')) {
        try {
          const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token_id: id })
          });
          const data = await response.json();
          if (response.ok) {
            document.getElementById(`tokenRow${id}`).remove();
            alert('Token deleted successfully');
          } else {
            alert(data.error || 'Deletion failed');
          }
        } catch (err) {
          alert('Network error');
        }
      }
    });
  });

  // Generate new token
  const generateBtn = document.getElementById('generateTokenBtn');
  if (generateBtn) {
    generateBtn.addEventListener('click', async function() {
      try {
        const response = await fetch('/apiToken/generate', { method: 'POST' });
        const data = await response.json();
        if (response.ok) {
          location.reload();
        } else {
          alert(data.error || 'Generation failed');
        }
      } catch (err) {
        alert('Network error');
      }
    });
  }

  // ---------- Bot Config: Collapsible Sections ----------
  document.querySelectorAll('.section-header').forEach(header => {
    header.addEventListener('click', () => {
      const sectionId = header.getAttribute('data-section');
      const content = document.getElementById(`section-${sectionId}`);
      const icon = header.querySelector('i');
      content.classList.toggle('hidden');
      icon.classList.toggle('rotate-180');
    });
  });

  // Add new target
  const addTargetBtn = document.getElementById('addTargetBtn');
  const newTargetInput = document.getElementById('new-target');
  const targetList = document.getElementById('target-list');
  const targetDropdown = document.getElementById('target-dropdown');

  function addTargetToList(targetName) {
    if (!targetName) return;
    const item = document.createElement('div');
    item.className = 'flex justify-between items-center p-2 bg-slate-100 dark:bg-slate-800 rounded';
    item.innerHTML = `
      <span>${escapeHtml(targetName)}</span>
      <button class="remove-target text-rose-500 hover:text-rose-700 text-sm"><i class="fas fa-times"></i></button>
    `;
    item.querySelector('.remove-target').addEventListener('click', () => item.remove());
    targetList.appendChild(item);
    // Add to dropdown if not exists
    let exists = false;
    for (let opt of targetDropdown.options) {
      if (opt.value === targetName) exists = true;
    }
    if (!exists) {
      const opt = document.createElement('option');
      opt.value = targetName;
      opt.textContent = targetName;
      targetDropdown.appendChild(opt);
    }
  }

  if (addTargetBtn && newTargetInput) {
    addTargetBtn.addEventListener('click', () => {
      const val = newTargetInput.value.trim();
      if (val) addTargetToList(val);
      newTargetInput.value = '';
    });
  }

  // Set Instructions
  const setInstructionsBtn = document.getElementById('setInstructionsBtn');
  if (setInstructionsBtn) {
    setInstructionsBtn.addEventListener('click', async () => {
      const target = targetDropdown.value;
      const attackType = document.getElementById('attack-type').value;
      const host = document.getElementById('host-input').value;
      if (!target || !attackType || !host) {
        alert('Please fill all fields');
        return;
      }
      // Simulate API call (replace with actual endpoint)
      alert(`Instructions set for ${target}: ${attackType} on ${host}`);
    });
  }

  // Set Connection
  const setConnectionBtn = document.getElementById('setConnectionBtn');
  const connectionType = document.getElementById('connection-type');
  const socketContainer = document.getElementById('socket-input-container');
  if (connectionType) {
    connectionType.addEventListener('change', () => {
      socketContainer.classList.toggle('hidden', connectionType.value !== 'socket');
    });
  }
  if (setConnectionBtn) {
    setConnectionBtn.addEventListener('click', () => {
      const type = connectionType.value;
      const socketDetail = document.getElementById('socket-input').value;
      if (!type) {
        alert('Select connection type');
        return;
      }
      if (type === 'socket' && !socketDetail) {
        alert('Enter socket details');
        return;
      }
      alert(`Connection set: ${type}${type === 'socket' ? ' - ' + socketDetail : ''}`);
    });
  }

  // ---------- Delete Account ----------
  const initiateDeleteBtn = document.getElementById('initiateDeleteBtn');
  const confirmDialog = document.getElementById('confirmationDialog');
  const cancelDeleteBtn = document.getElementById('cancelDeleteBtn');
  const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');

  function showConfirmationDialog() {
    confirmDialog.classList.remove('hidden');
    confirmDialog.classList.add('flex');
  }
  function hideConfirmationDialog() {
    confirmDialog.classList.add('hidden');
    confirmDialog.classList.remove('flex');
  }
  if (initiateDeleteBtn) {
    initiateDeleteBtn.addEventListener('click', () => {
      const password = document.getElementById('delete_password').value;
      const confirmation = document.getElementById('delete_confirmation').value;
      if (!password || confirmation !== 'DELETE') {
        alert('Please enter your password and type "DELETE" to confirm');
        return;
      }
      showConfirmationDialog();
    });
  }
  if (cancelDeleteBtn) cancelDeleteBtn.addEventListener('click', hideConfirmationDialog);
  if (confirmDeleteBtn) {
    confirmDeleteBtn.addEventListener('click', async () => {
      const form = document.getElementById('deleteAccountForm');
      const spinner = document.getElementById('deleteSpinner');
      if (spinner) spinner.classList.remove('hidden');
      try {
        const response = await fetch(form.action, {
          method: 'POST',
          body: new FormData(form)
        });
        if (response.redirected) {
          window.location.href = response.url;
        } else {
          const data = await response.json();
          alert(data.message || 'Account deleted');
          if (response.ok) window.location.href = '/';
        }
      } catch (err) {
        alert('Error deleting account');
      } finally {
        if (spinner) spinner.classList.add('hidden');
        hideConfirmationDialog();
      }
    });
  }

  // Helper escapeHtml (to prevent XSS)
  function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/[&<>]/g, function(m) {
      if (m === '&') return '&amp;';
      if (m === '<') return '&lt;';
      if (m === '>') return '&gt;';
      return m;
    });
  }
});