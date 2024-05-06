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

// JavaScript function to validate form before submission
function validateForm() {
    var titleInput = document.getElementById('title');
    var titleLength = titleInput.value.length;
    if (titleLength > 20) {
        alert('Title cannot exceed 20 characters!');
        titleInput.focus();
        return false;
    }

    var descriptionInput = document.getElementById('description');
    var descriptionLength = descriptionInput.value.length;
    if (descriptionLength > 500) {
        alert('Description cannot exceed 500 characters!');
        descriptionInput.focus();
        return false;
    }

    return true;
}
