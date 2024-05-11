// JavaScript function to update character counter for title input
document.getElementById('title').addEventListener('input', function() {
    var maxLength = this.getAttribute('maxlength');
    var currentLength = this.value.length;
    var remaining = maxLength - currentLength;
    document.getElementById('titleCounter').innerText = remaining;
});

// JavaScript function to update character counter for description textarea
document.getElementById('description').addEventListener('input', function() {
    var maxLength = this.getAttribute('maxlength');
    var currentLength = this.value.length;
    var remaining = maxLength - currentLength;
    document.getElementById('descriptionCounter').innerText = remaining;
});
//
document.querySelectorAll('.tag-btn').forEach(button => {
    button.addEventListener('click', function(event) {
        event.preventDefault(); // 阻止按钮的默认行为
        document.querySelectorAll('.tag-btn').forEach(btn => btn.classList.remove('selected'));
        this.classList.add('selected');
        document.getElementById('tag').value = this.getAttribute('data-tag');
    });
});