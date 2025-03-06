document.addEventListener('DOMContentLoaded', function() {
    const filterBtn = document.getElementById('filter-btn');
    const filterModal = document.getElementById('filter-modal');
    const capacitySlider = document.getElementById('capacity');
    const capacityValue = document.getElementById('capacity-value');
    const applyFilterBtn = document.getElementById('apply-filter');

    filterBtn.addEventListener('click', function() {
        filterModal.style.display = 'flex';
    });

    filterModal.addEventListener('click', function(event) {
        if (event.target === filterModal) {
            filterModal.style.display = 'none';
        }
    });

    applyFilterBtn.addEventListener('click', function() {
        // Add your filter logic here
        filterModal.style.display = 'none';
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const bookingModal = document.getElementById('booking-modal');
    const bookNowButtons = document.querySelectorAll('.action-btn');
    const confirmBookingButton = document.getElementById('confirm-booking');

    bookNowButtons.forEach(button => {
        button.addEventListener('click', () => {
            bookingModal.style.display = 'flex';
        });
    });

    confirmBookingButton.addEventListener('click', () => {
        // Add your booking confirmation logic here
        bookingModal.style.display = 'none';
    });

    // Close modal when clicking outside of it
    window.addEventListener('click', (event) => {
        if (event.target === bookingModal) {
            bookingModal.style.display = 'none';
        }
    });
});