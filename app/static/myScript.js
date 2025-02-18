
// This css file is an assignment of CITS5505 unit 
//in the university of Western Australia (2024 S1)

//This is the java script file, including different slient side validation



// function of userIsAuthenticated
document.addEventListener('DOMContentLoaded', function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// fucntion of requiring log in Modal, done by ChatGPT by asking it write modal function to alart on the login
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

//function to update character counter, done by ChatGPT by asking it write input counter
document.addEventListener('DOMContentLoaded', function () {
    var titleInput = document.getElementById('title');
    var descriptionInput = document.getElementById('description');
    
    if (titleInput) {
        titleInput.addEventListener('input', function() {
            var maxLength = this.getAttribute('maxlength');
            var currentLength = this.value.length;
            var remaining = maxLength - currentLength;
            document.getElementById('titleCounter').innerText = remaining;
        });
    }

    if (descriptionInput) {
        descriptionInput.addEventListener('input', function() {
            var maxLength = this.getAttribute('maxlength');
            var currentLength = this.value.length;
            var remaining = maxLength - currentLength;
            document.getElementById('descriptionCounter').innerText = remaining;
        });
    }
});


// function of client side validation: upload page, review the image to see if it meets the requirements
const fileInput = document.querySelector('input[type="file"]');


fileInput.addEventListener('change', (event) => {
    const selectedFile = event.target.files[0];
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];


    if (!allowedTypes.includes(selectedFile.type)) {

        alert('Only image files (jpg, jpeg, png, gif) are allowed.');
        fileInput.value = ''; 
    }
});

// function of  of client side validation: expression to check the email structure is valid at client side. If it is not valid return error to handle the exception.
document.getElementById('email').addEventListener('input', function() {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const emailHelpText = document.getElementById('emailHelp');
    if (this.value.match(emailPattern)) {
        emailHelpText.textContent = 'Email format is valid.';
        emailHelpText.style.color = 'green';
    } else {
        emailHelpText.textContent = 'Invalid email format.';
        emailHelpText.style.color = 'red';
    }
});


