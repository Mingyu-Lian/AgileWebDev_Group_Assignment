// function userIsAuthenticated() {
//     return document.body.dataset.userAuthenticated === 'true';
// }

document.addEventListener('DOMContentLoaded', function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const authRequiredLinks = document.querySelectorAll('.requires-auth');
    authRequiredLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            if (!userIsAuthenticated()) {
                event.preventDefault(); // Stop the default link behavior
                updateModalLoginLink(this.href);
                // Show modal
                var myModal = new bootstrap.Modal(document.getElementById('loginModal'));
                myModal.show();
            }
        });
    });

    function userIsAuthenticated() {
        return document.body.dataset.userAuthenticated === 'true';
    }

    function updateModalLoginLink(nextUrl) {
        const loginButton = document.querySelector('#loginModal .btn-primary');
        loginButton.href = `${loginButton.href}?next=${encodeURIComponent(nextUrl)}`;
    }
});