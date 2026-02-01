// Load header component
function loadHeader() {
    fetch('header-component.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('header-component').innerHTML = data;
            // Set active nav link based on current page
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
        .catch(error => console.error('Error loading header:', error));
}

// Helper function to show toast notifications
// Toast notifications are popups that appear briefly (top right corner) to inform the user of errors or other information.
function showToast(message) {
    $('#toastMessage').text(message);
    var toastEl = document.getElementById('errorToast');
    var toast = new bootstrap.Toast(toastEl, { autohide: true, delay: 4000 });
    toast.show();
}

// Load header when Page is ready
document.addEventListener('DOMContentLoaded', loadHeader);
