const menuBtn = document.getElementById('menu-btn');
const sidebar = document.getElementById('sidebar');

menuBtn.addEventListener('click', function() {
    sidebar.classList.toggle('hidden');
});

window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
        sidebar.classList.remove('hidden');
    } else {
        sidebar.classList.add('hidden');
    }
});

// Initial check on page load
if (window.innerWidth <= 768) {
    sidebar.classList.add('hidden');
}