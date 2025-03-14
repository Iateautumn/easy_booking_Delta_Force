document.addEventListener('DOMContentLoaded', async function () {
    viewApprovals();
});

viewApprovals();


async function getAllBookingRequests() {
    const apiUrl = '/admin/reservation/request';
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

async function approveBookingRequest(reservation_id) {
    const apiUrl = '/admin/reservation/approval';
    const userData = {
        "reservation_id": reservation_id
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

async function rejectBookingRequest(reservation_id) {
    const apiUrl = '/admin/reservation/reject';
    const userData = {
        "reservation_id": reservation_id
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

async function viewApprovals() {
    const approvals = await getAllBookingRequests();
    const approvalList = document.querySelector('.approval-list');
    const timeTable = [
        '8:00~8:45',
        '8:55~9:40',
        '9:50~10:35',
        '10:45~11:30',
        '11:40~12:25',
        '12:35~13:20',
        '13:30~14:15',
        '14:25~15:10',
        '15:20~16:05',
        '16:15~17:00'
      ];


    if (approvals.length > 0) {
        approvalList.innerHTML = '';
        approvals.forEach(approval => {
            const approvalCard = document.createElement('div');
            approvalCard.classList.add('approval-card');
            approvalCard.innerHTML = `
                <h1>Reservation ID: ${approval.reservationId}</h1>
                <h3>Room ${approval.classroomName}</h3>
                <p>Constrain: ${approval.constrain}</p>
                <h4>User: ${approval.username}</h4>
                <p>User Status: ${approval.userstatus}</p>
                <p>Date: ${approval.date}</p>
                <p>Time: ${timeTable[approval.timePeriod]}</p>
                
                <button class="action-btn" id="approve-request">Approve</button>
                <button class="action-btn" id="reject-request">Reject</button>
            `;
            approvalList.appendChild(approvalCard);
        });
    }

    const approveBtns = document.querySelectorAll('#approve-request');
    const rejectBtns = document.querySelectorAll('#reject-request');

    approveBtns.forEach((btn, index) => {
        btn.addEventListener('click', async () => {
            const reservation_id = approvals[index].reservationId;
            const result = await approveBookingRequest(reservation_id);
            if (result) {
                alert('Approved');
                viewApprovals();
            }
            else {
                alert('Error, Network Error');
            }
        });
    });

    rejectBtns.forEach((btn, index) => {
        btn.addEventListener('click', async () => {
            const reservation_id = approvals[index].reservationId;
            const result = await rejectBookingRequest(reservation_id);
            if (result) {
                alert('Rejected');
                viewApprovals();
            }
            else {
                alert('Error, Network Error');
            }
        });
    });

}