// Toggle section visibility
function toggleSection(sectionId) {
  const section = document.getElementById(sectionId);
  const toggleBtn = section.parentElement.querySelector('.toggle-btn');
  
  if (section.classList.contains('active')) {
    section.classList.remove('active');
    toggleBtn.classList.remove('rotate');
  } else {
    section.classList.add('active');
    toggleBtn.classList.add('rotate');
  }
}

// Add new target to the list
function addTarget() {
  const newTargetInput = document.getElementById('new-target');
  const targetList = document.getElementById('target-list');
  
  if (newTargetInput.value.trim() !== '') {
    const targetItem = document.createElement('div');
    targetItem.className = 'target-item';
    targetItem.innerHTML = `
      <span>${newTargetInput.value}</span>
      <button class="remove-btn" onclick="removeTarget(this)">REMOVE</button>
    `;
    
    targetList.appendChild(targetItem);
    newTargetInput.value = '';
  }
}

// Remove target from the list
function removeTarget(button) {
  const targetItem = button.parentElement;
  targetItem.remove();
}

// Toggle socket input based on connection type
function toggleSocketInput() {
  const connectionType = document.getElementById('connection-type').value;
  const socketInputContainer = document.getElementById('socket-input-container');
  
  if (connectionType === 'socket') {
    socketInputContainer.style.display = 'block';
  } else {
    socketInputContainer.style.display = 'none';
  }
}

// Set bot instructions
function setInstructions() {
  const attackType = document.getElementById('attack-type').value;
  const host = document.getElementById('host-input').value;
  
  if (attackType && host) {
    showToast(`INSTRUCTIONS SET:\nATTACK TYPE: ${attackType}\nTARGET HOST: ${host}`, "success");
  } else {
    showToast('PLEASE SELECT AN ATTACK TYPE AND ENTER A TARGET HOST', "error");
  }
}

// Set connection
function setConnection() {
  const connectionType = document.getElementById('connection-type').value;
  const socketInput = document.getElementById('socket-input').value;
  
  if (connectionType) {
    if (connectionType === 'socket' && !socketInput) {
      showToast('PLEASE ENTER SOCKET DETAILS FOR SOCKET CONNECTION', "error");
      return;
    }
    
    showToast(`CONNECTION SET:\nTYPE: ${connectionType}\n${connectionType === 'socket' ? 'SOCKET: ' + socketInput : ''}`, "success");
  } else {
    showToast('PLEASE SELECT A CONNECTION TYPE', "error");
  }
}

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
  // Add some example targets
  const exampleTargets = ['192.168.1.30', 'example.com', '10.0.0.5'];
  const targetList = document.getElementById('target-list');
  
  exampleTargets.forEach(target => {
    const targetItem = document.createElement('div');
    targetItem.className = 'target-item';
    targetItem.innerHTML = `
      <span>${target}</span>
      <button class="remove-btn" onclick="removeTarget(this)">REMOVE</button>
    `;
    
    targetList.appendChild(targetItem);
  });
});

// api_token genrate and delete
// API token generate/delete and DOM update
async function apiToken(endpoint, method, tokenId = null) {
  try {
    const response = await fetch(endpoint, { method });
    if (!response.ok) throw new Error('Failed to fetch API token');

    const data = await response.json();
    console.log(data.message);

    // Handle generate response
    if (data.api_token && data.id) {
      createTokenRow(data);
      showToast("NEW TOKEN GENERATED", "success");
    }

  } catch (error) {
    console.error("Error fetching API token:", error);
    showToast("API REQUEST FAILED", "error");
  }
}

function createTokenRow(data) {
  const tbody = document.querySelector("#tokenTableBody");
  const newRow = document.createElement("tr");
  newRow.id = `tokenRow${data.id}`;
  
  newRow.innerHTML = `
    <td>
      <div class="input-group">
        <input type="password" 
              id="tokenField${data.id}" 
              class="form-control tokenValue" 
              value="${escapeHtml(data.api_token)}" readonly>
        <div class="input-group-append">
          <button class="btn btn-outline" type="button" 
                  onclick="toggleToken('${data.id}')">
            <i class="fas fa-eye" id="toggleIcon${data.id}"></i>
          </button>
        </div>
      </div>
    </td>
    <td>
      <div class="btn-group">
        <button type="button" class="btn btn-outline" 
                onclick="copyToken('${data.id}')">
          <i class="fas fa-copy"></i> COPY
        </button>
        <button type="button" class="btn btn-outline" 
                onclick="apiTokenDelete(this, '${data.id}', '/apiToken/delete')">
          <i class="fas fa-trash"></i> DELETE
        </button>
      </div>
    </td>`;
  
  tbody.appendChild(newRow);
}

async function apiTokenDelete(btnEl, tokenId, endPoint) {
  try {
    const response = await fetch(`${endPoint}/${tokenId}`, { 
      method: 'DELETE' 
    });
    
    const data = await response.json().catch(() => ({}));
    
    if (!response.ok && !data.message?.toLowerCase().includes('deleted')) {
      throw new Error(data.error || 'Delete failed');
    }
    
    // Remove the exact row that contains the clicked button
    btnEl.closest('tr')?.remove();
    showToast('TOKEN DELETED SUCCESSFULLY', 'success');
    
  } catch (error) {
    console.error('Delete error:', error);
    showToast(error.message || 'FAILED TO DELETE TOKEN', 'error');
  }
}

// Utility function to prevent XSS
function escapeHtml(unsafe) {
  return unsafe
    ?.replace(/&/g, "&amp;")
    ?.replace(/</g, "&lt;")
    ?.replace(/>/g, "&gt;")
    ?.replace(/"/g, "&quot;")
    ?.replace(/'/g, "&#039;") || '';
}

// Tab functionality
function openTab(evt, tabName) {
  const contents = document.querySelectorAll(".tabcontent");
  const links = document.querySelectorAll(".tablinks");
  
  // Hide all tab contents
  contents.forEach(content => {
    content.style.display = "none";
    content.setAttribute("aria-hidden", "true");
  });
  
  // Deactivate all tab links
  links.forEach(link => {
    link.classList.remove("active");
    link.setAttribute("aria-selected", "false");
  });
  
  // Show the selected tab content
  document.getElementById(tabName).style.display = "block";
  document.getElementById(tabName).setAttribute("aria-hidden", "false");
  
  // Activate the clicked tab link
  evt.currentTarget.classList.add("active");
  evt.currentTarget.setAttribute("aria-selected", "true");
}

// Token visibility toggle
function toggleToken(id) {
  const field = document.getElementById(`tokenField${id}`);
  const icon = document.getElementById(`toggleIcon${id}`);

  if (field.type === "password") {
    field.type = "text";
    icon.classList.remove("fa-eye");
    icon.classList.add("fa-eye-slash");
  } else {
    field.type = "password";
    icon.classList.remove("fa-eye-slash");
    icon.classList.add("fa-eye");
  }
}

// Copy token to clipboard
function copyToken(id) {
  const field = document.getElementById(`tokenField${id}`);
  navigator.clipboard.writeText(field.value.trim()).then(() => {
    showToast("API TOKEN COPIED TO CLIPBOARD!", "success");
  }).catch(err => {
    showToast("FAILED TO COPY TOKEN", "error");
    console.error("Failed to copy token:", err);
  });
}

// Password strength checker
function checkPasswordStrength(password) {
  const strengthBar = document.getElementById("passwordStrength");
  const lengthHint = document.getElementById("lengthHint");
  const numberHint = document.getElementById("numberHint");
  const specialHint = document.getElementById("specialHint");
  
  let strength = 0;
  
  // Length check
  if (password.length >= 8) {
    strength += 1;
    lengthHint.classList.remove("text-muted");
    lengthHint.classList.add("text-success");
  } else {
    lengthHint.classList.remove("text-success");
    lengthHint.classList.add("text-muted");
  }
  
  // Number check
  if (/\d/.test(password)) {
    strength += 1;
    numberHint.classList.remove("text-muted");
    numberHint.classList.add("text-success");
  } else {
    numberHint.classList.remove("text-success");
    numberHint.classList.add("text-muted");
  }
  
  // Special character check
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    strength += 1;
    specialHint.classList.remove("text-muted");
    specialHint.classList.add("text-success");
  } else {
    specialHint.classList.remove("text-success");
    specialHint.classList.add("text-muted");
  }
  
  // Update strength bar
  const width = (strength / 3) * 100;
  strengthBar.style.width = `${width}%`;
  
  if (strength === 0) {
    strengthBar.style.backgroundColor = "#ff0033";
  } else if (strength === 1) {
    strengthBar.style.backgroundColor = "#ff0033";
  } else if (strength === 2) {
    strengthBar.style.backgroundColor = "#ffcc00";
  } else {
    strengthBar.style.backgroundColor = "#00ff41";
  }
}

// Password match checker
function checkPasswordMatch() {
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirm_password").value;
  const feedback = document.getElementById("passwordMatchFeedback");
  
  if (password && confirmPassword && password !== confirmPassword) {
    feedback.style.display = "block";
    document.getElementById("confirm_password").setCustomValidity("Passwords do not match");
  } else {
    feedback.style.display = "none";
    document.getElementById("confirm_password").setCustomValidity("");
  }
}

// Confirmation dialog for account deletion
function showConfirmationDialog() {
  const form = document.getElementById("deleteAccountForm");
  const password = document.getElementById("delete_password").value;
  const confirmation = document.getElementById("delete_confirmation").value;
  
  if (!password) {
    showToast("PLEASE ENTER YOUR PASSWORD", "error");
    return;
  }
  
  if (confirmation !== "DELETE") {
    showToast('PLEASE TYPE "DELETE" TO CONFIRM', "error");
    return;
  }
  
  document.getElementById("confirmationDialog").style.display = "flex";
}

function hideConfirmationDialog() {
  document.getElementById("confirmationDialog").style.display = "none";
}

function submitDeleteAccount() {
  const spinner = document.getElementById("deleteSpinner");
  spinner.style.display = "inline-block";
  
  // Submit the form
  document.getElementById("deleteAccountForm").submit();
}

// Form submission handler
document.getElementById("userInfoForm").addEventListener("submit", function(e) {
  const spinner = document.getElementById("updateSpinner");
  spinner.style.display = "inline-block";
});

// Show toast notification
function showToast(message, type = "info") {
  const toast = document.createElement("div");
  toast.className = `toast-notification toast-${type}`;
  toast.setAttribute("role", "alert");
  toast.innerHTML = `
    <div class="toast-message">${message}</div>
    <button class="toast-close" onclick="this.parentElement.remove()" aria-label="Close notification">
      <i class="fas fa-times"></i>
    </button>
  `;
  
  document.body.appendChild(toast);
  
  // Auto-remove after 5 seconds
  setTimeout(() => {
    toast.classList.add("fade-out");
    setTimeout(() => toast.remove(), 300);
  }, 5000);
}

// Initialize default tab
document.addEventListener("DOMContentLoaded", function() {
  document.getElementById("defaultOpen").click();
  
  // Add toast notification styles dynamically
  const toastStyles = document.createElement("style");
  toastStyles.innerHTML = `
    .toast-notification {
      position: fixed;
      bottom: 20px;
      right: 20px;
      padding: 15px 20px;
      border-radius: 6px;
      color: white;
      display: flex;
      align-items: center;
      justify-content: space-between;
      max-width: 350px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
      z-index: 10000;
      transform: translateY(100px);
      opacity: 0;
      animation: toastSlideIn 0.3s ease forwards;
      font-family: 'JetBrains Mono', monospace;
      border: 1px solid;
    }
    
    .toast-info {
      background: rgba(0, 136, 255, 0.2);
      border-color: rgba(0, 136, 255, 0.5);
    }
    
    .toast-success {
      background: rgba(0, 255, 65, 0.2);
      border-color: rgba(0, 255, 65, 0.5);
    }
    
    .toast-error {
      background: rgba(255, 0, 51, 0.2);
      border-color: rgba(255, 0, 51, 0.5);
    }
    
    .toast-warning {
      background: rgba(255, 204, 0, 0.2);
      border-color: rgba(255, 204, 0, 0.5);
      color: #333;
    }
    
    .toast-close {
      background: none;
      border: none;
      color: inherit;
      margin-left: 15px;
      cursor: pointer;
      opacity: 0.8;
    }
    
    .toast-close:hover {
      opacity: 1;
    }
    
    .fade-out {
      animation: toastFadeOut 0.3s ease forwards !important;
    }
    
    @keyframes toastSlideIn {
      to {
        transform: translateY(0);
        opacity: 1;
      }
    }
    
    @keyframes toastFadeOut {
      to {
        transform: translateY(100px);
        opacity: 0;
      }
    }
  `;
  document.head.appendChild(toastStyles);
});