

function toggleMenu() {
    const menu = document.getElementById('sideMenu');
const backdrop = document.querySelector('.menu-backdrop');
menu.classList.toggle('active');
backdrop.classList.toggle('active');
}