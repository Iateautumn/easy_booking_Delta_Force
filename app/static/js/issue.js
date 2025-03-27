document.addEventListener('DOMContentLoaded', async function () {
    viewIssues();
});

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
    const apiUrl = '/admin/issue/report/delete';
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

async function viewIssues() {
    const issues = await getRoomIssue();
    const issueList = document.querySelector('.issue-list');
    const loading_item = document.getElementById('loading-item');

    if(issues.length > 0) {
        issueList.innerHTML = '';
        issues.forEach(issue => {
            const issueCard = document.createElement('div');
            issueCard.classList.add('issue-card');
            issueCard.innerHTML = `
                <h3>Issue ID: ${issue.issueId}</h3>
                <p>Issue: ${issue.issue}</p>
                <p>Reported by: ${issue.userName}</p>
                <p>Date Reported: ${issue.date}</p>
                <button class="action-btn" id="remove-issue">Remove</button>
            `;
            issueList.appendChild(issueCard);
        });
    }
    
    const removeBtns = document.querySelectorAll('#remove-issue');
    removeBtns.forEach((btn, index) => {
        btn.addEventListener('click', async () => {
            const issue_id = issues[index].issueId;

            issueList.innerHTML = '';

            loading_item.style.display = 'flex';
            document.getElementById('loading-hint').innerText = 'Removing...';

            const result = await removeRoomIssue(issue_id);

            document.getElementById('loading-hint').innerText = 'Loading Issues...';

            if (result) {
                alert('Removed');
                viewIssues();
            }
            else {
                alert('Error, Network Error');
                viewIssues();
            }
        });
    });

    loading_item.style.display = 'none';
}