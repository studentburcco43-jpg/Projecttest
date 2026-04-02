// This function loads the header component from the header-component.html file into the page.
function loadHeader() {
    // This uses the fetch API to request the content of the header-component.html file from the server.
    fetch('header-component.html')
        // This processes the server response as plain text.
        .then(response => response.text())
        // This takes the text content and inserts it into the HTML element with the ID 'header-component'.
        .then(data => {
            document.getElementById('header-component').innerHTML = data;
            // This determines the current page by extracting the last part of the URL path, defaulting to 'index.html' if empty.
            const currentPage = window.location.pathname.split('/').pop() || 'index.html';
            // This selects all navigation link elements on the page.
            const navLinks = document.querySelectorAll('.nav-link');
            // This loops through each navigation link to check if it matches the current page.
            navLinks.forEach(link => {
                // This checks if the link's href attribute matches the current page.
                if (link.getAttribute('href') === currentPage) {
                    // This adds the 'active' class to highlight the current page link.
                    link.classList.add('active');
                    // This sets the aria-current attribute for accessibility, indicating the current page.
                    link.setAttribute('aria-current', 'page');
                } else {
                    // This removes the 'active' class from non-current links.
                    link.classList.remove('active');
                    // This removes the aria-current attribute from non-current links.
                    link.removeAttribute('aria-current');
                }
            });
        })
        // This handles any errors that occur during the fetch request.
        .catch(error => {
            // This logs the error to the console for debugging purposes.
            console.error('Error loading header:', error);
            // This provides a fallback header markup if the fetch fails, such as when the file is opened locally or the server is not running.
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

// This function displays a toast notification popup to show messages to the user.
function showToast(message) {
    // This gets the HTML element where the toast message will be displayed.
    var msgEl = document.getElementById('toastMessage');
    // This sets the text content of the message element to the provided message, if the element exists.
    if (msgEl) msgEl.textContent = message;
    // This gets the toast HTML element.
    var toastEl = document.getElementById('errorToast');
    // This checks if the toast element exists and if Bootstrap is available.
    if (toastEl && typeof bootstrap !== 'undefined') {
        // This creates a new Bootstrap toast instance with auto-hide enabled and a 4-second delay.
        var toast = new bootstrap.Toast(toastEl, { autohide: true, delay: 4000 });
        // This shows the toast notification.
        toast.show();
    } else {
        // This provides a fallback by logging the message to the console if Bootstrap is not available.
        console.info('Toast:', message);
    }
}

// This adds an event listener that runs the loadHeader function when the page's DOM content has finished loading.
document.addEventListener('DOMContentLoaded', loadHeader);
