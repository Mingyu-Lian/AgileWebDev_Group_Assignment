// change page
function ChangePage(pageId, clickedLink) {
    document.querySelectorAll('.page').forEach(function(el) {
        el.style.display = 'none';
    });
    document.getElementById(pageId).style.display = 'block';


}