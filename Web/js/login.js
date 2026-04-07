// Initialize the page when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    loadHeader();
    setupLoginForm();
    setupPasswordToggle();
});

// Setup login form validation and submit
function setupLoginForm() {
    const loginForm = document.getElementById('loginForm');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const loginBtn = document.getElementById('loginBtn');
    const loginSpinner = document.getElementById('loginSpinner');
    const btnText = document.querySelector('.btn-text');

    if (!loginForm) return;

    // Real-time validation as user types
    usernameInput.addEventListener('blur', validateUsername);
    passwordInput.addEventListener('blur', validatePassword);

    // Clear error messages when user starts typing
    usernameInput.addEventListener('input', function() {
        if (this.classList.contains('is-invalid')) {
            this.classList.remove('is-invalid');
            document.getElementById('usernameError').textContent = '';
        }
    });

    passwordInput.addEventListener('input', function() {
        if (this.classList.contains('is-invalid')) {
            this.classList.remove('is-invalid');
            document.getElementById('passwordError').textContent = '';
        }
    });
 
    // Handle form submission
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Validate both fields
        const usernameValid = validateUsername();
        const passwordValid = validatePassword();

        if (!usernameValid || !passwordValid) {
            return;
        }

        // Disable button and show spinner
        loginBtn.disabled = true;
        loginSpinner.classList.remove('d-none');
        btnText.textContent = 'Signing in...';

        try {
            await loginUser(usernameInput.value, passwordInput.value);

            // Save preference if remember me is checked
            if (document.getElementById('rememberMe').checked) {
                localStorage.setItem('rememberedUsername', usernameInput.value);
            } else {
                localStorage.removeItem('rememberedUsername');
            }

            // Redirect on success
            window.location.href = 'index.html';

        } catch (error) {
            showErrorMessage(error.message);
            loginBtn.disabled = false;
            loginSpinner.classList.add('d-none');
            btnText.textContent = 'Sign In';
        }
    });
}

// Validate username
function validateUsername() {
    const usernameInput = document.getElementById('username');
    const usernameError = document.getElementById('usernameError');
    const username = usernameInput.value.trim();

    if (!username) {
        usernameInput.classList.add('is-invalid');
        usernameError.textContent = 'Username is required';
        return false;
    } else {
        usernameInput.classList.remove('is-invalid');
        usernameError.textContent = '';
        return true;
    }
}

// Validate password
function validatePassword() {
    const passwordInput = document.getElementById('password');
    const passwordError = document.getElementById('passwordError');
    const password = passwordInput.value;

    if (!password) {
        passwordInput.classList.add('is-invalid');
        passwordError.textContent = 'Password is required';
        return false;
    } else if (password.length < 6) {
        passwordInput.classList.add('is-invalid');
        passwordError.textContent = 'Password must be at least 6 characters';
        return false;
    } else {
        passwordInput.classList.remove('is-invalid');
        passwordError.textContent = '';
        return true;
    }
}

// Toggle password visibility
function setupPasswordToggle() {
    const toggleBtn = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');

    if (!toggleBtn || !passwordInput) return;

    toggleBtn.addEventListener('click', function(e) {
        e.preventDefault();
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
    });
}

// Call the FastAPI login endpoint and return a resolved promise on success
function loginUser(username, password) {
    return fetch('/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
    }).then(async resp => {
        if (resp.ok) {
            return Promise.resolve();
        }
        const data = await resp.json().catch(() => ({}));
        throw new Error(data.detail || 'Login failed');
    });
}

// Show error message using toast or inline alert
function showErrorMessage(message) {
    const loginError = document.getElementById('loginError');
    if (loginError) {
        loginError.textContent = message;
        loginError.classList.remove('d-none');
        return;
    }
    const toast = document.getElementById('errorToast');
    const toastMessage = document.getElementById('toastMessage');
    if (toast && toastMessage) {
        toastMessage.textContent = message;
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
    }
}

// Show success message
function showSuccessMessage(message) {
    const toastContainer = document.querySelector('.toast-container');
    if (toastContainer) {
        const successToast = document.createElement('div');
        successToast.className = 'toast align-items-center text-bg-success border-0 show';
        successToast.setAttribute('role', 'alert');
        successToast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        toastContainer.appendChild(successToast);

        setTimeout(() => {
            successToast.remove();
        }, 3000);
    }
}

// Load remembered username if it exists
document.addEventListener('DOMContentLoaded', function() {
    const rememberedUsername = localStorage.getItem('rememberedUsername');
    if (rememberedUsername) {
        const usernameInput = document.getElementById('username');
        const rememberMeCheckbox = document.getElementById('rememberMe');
        if (usernameInput && rememberMeCheckbox) {
            usernameInput.value = rememberedUsername;
            rememberMeCheckbox.checked = true;
        }
    }
});

// Prevent form submission on Enter if validation fails
document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('password');
    if (passwordInput) {
        passwordInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const loginForm = document.getElementById('loginForm');
                if (loginForm) {
                    loginForm.dispatchEvent(new Event('submit'));
                }
            }
        });
    }
});


