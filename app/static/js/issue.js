




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

async function viewIssues() {
    const issues = await getRoomIssue();

    const issueList = document.getElementById('issue-list');

    if(issues.length > 0) {
        issueList.innerHTML = '';
        issues.forEach(issue => {
            const issueCard = document.createElement('div');
            issueCard.classList.add('issue-card');
            issueCard.innerHTML = `
                <h3>Issue ID: ${issue.issueId}</h3>
                <p>Issue: ${issue.issue}</p>
                <p>Reported by: ${issue.username}</p>
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
            const result = await removeRoomIssue(issue_id);
            if (result) {
                alert('Removed');
                viewIssues();
            }
            else {
                alert('Error, Network Error');
            }
        });
    });


}