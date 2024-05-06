// JavaScript function to update character counter for title input
document.getElementById('title').addEventListener('input', function() {
    var maxLength = this.maxLength;
    var currentLength = this.value.length;
    var remaining = maxLength - currentLength;
    document.getElementById('titleCounter').innerText = remaining;
});

// JavaScript function to update character counter for description textarea
document.getElementById('description').addEventListener('input', function() {
    var maxLength = this.maxLength;
    var currentLength = this.value.length;
    var remaining = maxLength - currentLength;
    document.getElementById('descriptionCounter').innerText = remaining;
});

const buttons = document.querySelectorAll('.tag-btn');

        buttons.forEach(button => {
            button.addEventListener('click', () => {
                button.classList.toggle('selected');
            });
        });