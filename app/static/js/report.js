document.addEventListener('DOMContentLoaded', async function () {
    const exportBtn = document.getElementById('export-report-btn');
    exportBtn.addEventListener('click', async function () {
        await getReportPDF();
    });
    viewReport();
});





async function getReport() {
    const apiUrl = '/admin/report/analysis';
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
                return Data.data;
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

async function getReportPDF() {
    const apiUrl = '/admin/report/analysis/export';
    await fetch(apiUrl)
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'all_reservation.ics';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(error => console.error('Error:', error));
}

async function viewReport() {
    const reports = await getReport();
    const reportList = document.querySelector('.report-list');

    if (reports.length > 0) {
        reportList.innerHTML = '';
        reports.forEach(report => {
            const reportCard = document.createElement('div');
            reportCard.className = 'report-card';
            reportCard.innerHTML = `
                <div class="report-text">
                    <h3>${report.roomName}</h3>
                    <p>Weekly Usage: ${report.usage}%</p>
                </div>
                <div class="report-img>
                    <img src="${report.heatGraph}" alt="Heat Graph">
                </div>
            `;
            reportList.appendChild(reportCard);
        })
    }
}