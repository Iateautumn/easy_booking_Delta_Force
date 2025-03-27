document.addEventListener('DOMContentLoaded', function() {
    const bookingDate = document.getElementById('booking-date');
    const today = new Date();
    
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0'); 
    const day = String(today.getDate()).padStart(2, '0'); 
    
    const minDate = `${year}-${month}-${day}`;
    bookingDate.setAttribute('min', minDate);} );


function toggleMenu() {
    const menu = document.getElementById('sideMenu');
const backdrop = document.querySelector('.menu-backdrop');
menu.classList.toggle('active');
backdrop.classList.toggle('active');
}

