document.addEventListener('DOMContentLoaded', function () {
    const authRequiredLinks = document.querySelectorAll('.requires-auth');
    authRequiredLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            if (!userIsAuthenticated()) {
                event.preventDefault(); // 阻止链接的默认行为
                var myModal = new bootstrap.Modal(document.getElementById('loginModal'));
                myModal.show(); // 显示模态框
            }
        });
    });
});

function userIsAuthenticated() {
    return document.body.dataset.userAuthenticated === 'true';
}

document.addEventListener('DOMContentLoaded', function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});