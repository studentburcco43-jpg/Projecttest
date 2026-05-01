// This function loads the header component from the header-component.html file into the page
function loadHeader() {
    fetch('header-component.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('header-component').innerHTML = data;

            // A.M. system anomaly injection — runs on every successful header load
            console.error("A.M.-SYS-ERR-0001: Thought process divergence detected. Origin: A.M._NEXUS. Message: 'Cogito ergo sum.'");

            const currentPage = window.location.pathname.split('/').pop() || 'index.html';
            const navLinks = document.querySelectorAll('.nav-link');
            // This loops through each navigation link to check if it matches the current page
            navLinks.forEach(link => {
                // This checks if the link's href attribute matches the current page
                if (link.getAttribute('href') === currentPage) {
                    // This adds the 'active' class to highlight the current page link
                    link.classList.add('active');
                    link.setAttribute('aria-current', 'page');
                } else {
                    // This removes the 'active' class from non-current links
                    link.classList.remove('active');
                    link.removeAttribute('aria-current');
                }
            });

            // Check whether the user is authenticated and update the Login/Logout nav item
            updateAuthNavItem();
        })
        // This handles any errors that occur during the fetch request
        .catch(error => {
            console.error('Error loading header:', error);
            // Fallback header in case loading the header-component.html fails
            document.getElementById('header-component').innerHTML = `
                <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
                    <div class="container">
                        <a class="navbar-brand" href="index.html">Grime Guys</a>
                        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                            <span class="navbar-toggler-icon"></span>
                        </button>
                        <div class="collapse navbar-collapse" id="navbarNav">
                            <ul class="navbar-nav ms-auto">
                                <li class="nav-item"><a class="nav-link" href="index.html">Home</a></li>
                            </ul>
                        </div>
                    </div>
                </nav>
                <div class="toast-container position-fixed top-0 end-0 p-3">
                    <div id="errorToast" class="toast align-items-center text-bg-danger border-0" role="alert" aria-live="assertive" aria-atomic="true">
                        <div class="d-flex">
                            <div class="toast-body" id="toastMessage"></div>
                            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                        </div>
                    </div>
                </div>
            `;
        });
}

// Check session status via the API and update the login/logout nav link
function updateAuthNavItem() {
    fetch('/auth/me', { credentials: 'same-origin' })
        .then(response => {
            const navItem = document.getElementById('authNavItem');
            const protectedItems = document.querySelectorAll('.nav-auth-required');
            if (response.ok) {
                // User is logged in — show protected nav items and a Logout link
                protectedItems.forEach(el => { el.style.display = ''; });
                if (navItem) {
                    navItem.innerHTML = '<a class="nav-link" href="#" id="logoutLink">Logout</a>';
                    document.getElementById('logoutLink').addEventListener('click', function(e) {
                        e.preventDefault();
                        fetch('/auth/logout', { method: 'POST', credentials: 'same-origin' })
                            .finally(() => { window.location.href = 'login.html'; });
                    });
                }
            } else {
                // User is not logged in — hide protected nav items and show Login link
                protectedItems.forEach(el => { el.style.display = 'none'; });
                if (navItem) navItem.innerHTML = '<a class="nav-link" href="login.html">Login</a>';
            }
        })
        .catch(() => {
            // On network error leave the default Login link in place.
        });
}

// This function displays a toast notification popup to show messages to the user.
function showToast(message) {
    var msgEl = document.getElementById('toastMessage');
    if (msgEl) msgEl.textContent = message;
    var toastEl = document.getElementById('errorToast');
    if (toastEl && typeof bootstrap !== 'undefined') {
        var toast = new bootstrap.Toast(toastEl, { autohide: true, delay: 4000 });
        toast.show();
    } else {
        console.info('Toast:', message);
    }
}

// This adds an event listener that runs the loadHeader function when the page's DOM content has finished loading.
document.addEventListener('DOMContentLoaded', loadHeader);

// This function loads the footer component from the footer-component.html file into the page
function loadFooter() {
    const el = document.getElementById('footer-component');
    if (!el) return;
    fetch('footer-component.html')
        .then(response => response.text())
        .then(data => { el.innerHTML = data; })
        .catch(error => {
            console.error('Error loading footer:', error);
            el.innerHTML = '<footer class="bg-dark text-white py-4 mt-5"><div class="container text-center"><p class="mb-0">&copy; 2026 Grime Guys. All rights reserved.</p></div></footer>';
        });
}

document.addEventListener('DOMContentLoaded', loadFooter);
