document.addEventListener('DOMContentLoaded', function () {
    const bookingDate = document.getElementById('booking-date');
    const today = new Date();

    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');

    const minDate = `${year}-${month}-${day}`;
    if (bookingDate) {
        bookingDate.setAttribute('min', minDate);
    }

    handleProfile();
});

function toggleMenu() {
    const menu = document.getElementById('sideMenu');
    const backdrop = document.querySelector('.menu-backdrop');
    menu.classList.toggle('active');
    backdrop.classList.toggle('active');
}

async function getProfile() {

    const apiUrl = '/auth/profile';

    const response = await fetch(apiUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    const Data = await response.json();

    if (Data) {
        switch (Data.code) {
            case 200:
                return Array.isArray(Data.data) ? Data.data : [];
            default:
                alert(`Error, (${Data.message})`);
                return [];
        }
    } else {
        alert('Error, Network Error');
        return [];
    }
}

async function handleProfile() {

    const profiles = document.querySelectorAll('.profile');
    const userData = await getProfile();

    console.log(userData);


    if (userData.length > 0) {
        profiles.forEach(profile => {
            profile.innerHTML = `

                <img src="../../static/icon/profile.svg" class="icon" alt="Logout Icon">
                Welcome, ${userData[0].username}(${userData[0].status})!
            `;
        });
    }
    else {
        alert('Error, profile fetch failed');
    }

}
