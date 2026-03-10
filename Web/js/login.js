// Initialize the page when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    loadHeader();
    setupLoginForm();
    setupPasswordToggle();
});

// Setup login form validation and submit
function setupLoginForm() {
    const loginForm = document.getElementById('loginForm');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const loginBtn = document.getElementById('loginBtn');
    const loginSpinner = document.getElementById('loginSpinner');
    const btnText = document.querySelector('.btn-text');

    if (!loginForm) return;

    // Real-time validation as user types
    emailInput.addEventListener('blur', validateEmail);
    passwordInput.addEventListener('blur', validatePassword);

    // Clear error messages when user starts typing
    emailInput.addEventListener('input', function() {
        if (this.classList.contains('is-invalid')) {
            this.classList.remove('is-invalid');
            document.getElementById('emailError').textContent = '';
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
        const emailValid = validateEmail();
        const passwordValid = validatePassword();

        if (!emailValid || !passwordValid) {
            return;
        }

        // Disable button and show spinner
        loginBtn.disabled = true;
        loginSpinner.classList.remove('d-none');
        btnText.textContent = 'Signing in...';

        try {
            // Simulate API call (replace with actual backend call)
            await simulateLogin(emailInput.value, passwordInput.value);

            // Show success message
            showSuccessMessage('Login successful! Redirecting...');

            // Save preference if remember me is checked
            if (document.getElementById('rememberMe').checked) {
                localStorage.setItem('rememberedEmail', emailInput.value);
            } else {
                localStorage.removeItem('rememberedEmail');
            }

            // Redirect after 1.5 seconds
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 1500);

        } catch (error) {
            showErrorMessage(error.message);
            loginBtn.disabled = false;
            loginSpinner.classList.add('d-none');
            btnText.textContent = 'Sign In';
        }
    });
}

// Validate email format
function validateEmail() {
    const emailInput = document.getElementById('email');
    const emailError = document.getElementById('emailError');
    const email = emailInput.value.trim();

    // Simple email validation regex
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!email) {
        emailInput.classList.add('is-invalid');
        emailError.textContent = 'Email is required';
        return false;
    } else if (!emailRegex.test(email)) {
        emailInput.classList.add('is-invalid');
        emailError.textContent = 'Please enter a valid email address';
        return false;
    } else {
        emailInput.classList.remove('is-invalid');
        emailError.textContent = '';
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

// Simulate login API call (replace with actual backend call)
function simulateLogin(email, password) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            // Demo credentials
            if (email === 'demo@grimeguys.com' && password === 'demo123') {
                // Store user session (in real app, store JWT token)
                sessionStorage.setItem('userEmail', email);
                sessionStorage.setItem('isLoggedIn', 'true');
                sessionStorage.setItem('loginTime', new Date().toISOString());
                resolve();
            } else {
                reject(new Error('Invalid email or password. Try demo@grimeguys.com / demo123'));
            }
        }, 1000); // Simulate network delay
    });
}

// Show error message using toast
function showErrorMessage(message) {
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
    // Create a temporary success toast
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

        // Auto remove after 3 seconds
        setTimeout(() => {
            successToast.remove();
        }, 3000);
    }
}

// Load remembered email if it exists
document.addEventListener('DOMContentLoaded', function() {
    const rememberedEmail = localStorage.getItem('rememberedEmail');
    if (rememberedEmail) {
        const emailInput = document.getElementById('email');
        const rememberMeCheckbox = document.getElementById('rememberMe');
        if (emailInput && rememberMeCheckbox) {
            emailInput.value = rememberedEmail;
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
