// function userIsAuthenticated


document.addEventListener('DOMContentLoaded', function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});


// require log in
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


// JavaScript function to update character counter 
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

// 获取文件上传控件
const fileInput = document.querySelector('input[type="file"]');

// 监听文件选择事件
fileInput.addEventListener('change', (event) => {
    const selectedFile = event.target.files[0];
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];

    // 检查所选文件类型是否在允许的文件类型列表中
    if (!allowedTypes.includes(selectedFile.type)) {
        // 不允许的文件类型，显示提示信息并清除文件选择
        alert('Only image files (jpg, jpeg, png, gif) are allowed.');
        fileInput.value = ''; // 清除文件选择
    }
});
