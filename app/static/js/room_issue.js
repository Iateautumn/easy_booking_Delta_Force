async function getRoomIssue() {
    const apiUrl = '/admin/issue/all';
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
    }
    else {
        alert('Error, Network Error');
        return [];
    }
}

async function removeRoomIssue(issue_id) {
    const apiUrl = '/admin/issue/remove';
    const userData = {
        "issue_id": issue_id
    };

    const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    });

    const Data = await response.json();

    if (Data) {
        switch (Data.code) {
            case 200:
                return true;
            default:
                alert(`Error, (${Data.message})`);
                return false;
        }
    }
    else {
        alert('Error, Network Error');
        return false;
    }
}

async function userReportIssue(issue){
    const apiUrl = '/user/classroom/issue/report';
    const userData = {
        "issue": issue
    };

    const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    });

    const Data = await response.json();

    if (Data) {
        switch (Data.code) {
            case 200:
                return true;
            default:
                alert(`Error, (${Data.message})`);
                return false;
        }
    }
    else {
        alert('Error, Network Error');
        return false;
    }
}