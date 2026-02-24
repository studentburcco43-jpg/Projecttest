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
        .catch(error => console.error('Error loading header:', error));
}

// Display a toast notification popup to show messages to the user
function showToast(message) {
    $('#toastMessage').text(message);
    var toastEl = document.getElementById('errorToast');
    var toast = new bootstrap.Toast(toastEl, { autohide: true, delay: 4000 });
    toast.show();
}

// Run the loadHeader function when the page finishes loading
document.addEventListener('DOMContentLoaded', loadHeader);
