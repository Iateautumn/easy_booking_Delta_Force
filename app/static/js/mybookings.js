async function getAllMyBookings() {
    const apiUrl = '/api/mybookings';
    const response = await fetch(apiUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });
    
    const data = await response.json();

    if (data) {
        switch (data.code) {
            case 200:
                return Array.isArray(data.data) ? data.data : [];
            default:
                alert(`Error, (${data.message})`);
                return [];
        }
    }
}