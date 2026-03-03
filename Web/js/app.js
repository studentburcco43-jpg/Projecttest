// Load the header component from header-component.html file into the page
function loadHeader() {
    fetch('header-component.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('header-component').innerHTML = data;
            // Highlight the current page link in the navigation menu as active
            const currentPage = window.location.pathname.split('/').pop() || 'index.html';
            const navLinks = document.querySelectorAll('.nav-link');
            navLinks.forEach(link => {
                if (link.getAttribute('href') === currentPage) {
                    link.classList.add('active');
                    link.setAttribute('aria-current', 'page');
                } else {
                    link.classList.remove('active');
                    link.removeAttribute('aria-current');
                }
            });
        })
        .catch(error => {
            console.error('Error loading header:', error);
            // Fallback header markup if fetch fails (e.g., opened via file:// or server not running)
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
                                <li class="nav-item"><a class="nav-link" href="services.html">Services</a></li>
                                <li class="nav-item"><a class="nav-link" href="Job.html">Job Summary</a></li>
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

// Display a toast notification popup to show messages to the user
function showToast(message) {
    var msgEl = document.getElementById('toastMessage');
    if (msgEl) msgEl.textContent = message;
    var toastEl = document.getElementById('errorToast');
    if (toastEl && typeof bootstrap !== 'undefined') {
        var toast = new bootstrap.Toast(toastEl, { autohide: true, delay: 4000 });
        toast.show();
    } else {
        // Fallback: briefly flash message in console
        console.info('Toast:', message);
    }
}

// Run the loadHeader function when the page finishes loading
document.addEventListener('DOMContentLoaded', loadHeader);
