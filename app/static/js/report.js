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
    } else {
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
            a.download = 'report.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(error => console.error('Error:', error));
}

async function viewReport() {
    const reports = await getReport();
    const reportList = document.querySelector('.report-list');

    if (reports) {
        const dates = reports.jointData.dates;
        const matrix = reports.jointData.matrix;
        const jointReport = document.createElement('div');
        jointReport.classList.add('report-card');
        jointReport.innerHTML = `
        <div class="heatmap-container">
            <h2>All Rooms Heatmap</h2>
            <div class="legend">
                <span class="legend-item" data-range="0-1"></span> 0 - 1
                <span class="legend-item" data-range="2-3"></span> 2 - 3
                <span class="legend-item" data-range="3-6"></span> 3 - 6
                <span class="legend-item" data-range=">6"></span> > 6
            </div>
            <div id="heatmap"></div>
        </div>
        `;
        reportList.appendChild(jointReport);
        // const chartDom = document.getElementById('main-chart');
        // const myChart = echarts.init(chartDom);
        // var option;
        // var data = [];

        const bookingsData = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ];

        for (var i = 0; i < matrix.length; i++) {
            for (var j = 0; j < matrix[i].length; j++) {
                bookingsData[i][j] = matrix[i][j];
            }
        }

        // option = {
        //     title: {
        //         top: 0,
        //         left: 'left',
        //         text: 'All Rooms Heatmap',
        //         textStyle: {
        //             color: '#13439b'
        //         }
        //     },
        //     tooltip: {
        //         formatter: function (params) {
        //             return String(params.value[1]);
        //         }
        //     },
        //     visualMap: {
        //         show: true,
        //         inRange: {
        //             color: ['#b0cbfc', '#13439b']
        //         },
        //         type: 'piecewise',
        //         pieces: [
        //             {min: 0, max: 1},
        //             {min: 2, max: 3},
        //             {min: 3, max: 6},
        //             {min: 6},
        //         ],
        //         orient: 'horizontal',
        //         left: 'left',
        //         top: 30
        //     },
        //     calendar: {
        //         itemStyle: {
        //             color: '#EBEDF0',
        //             borderWidth: 3,
        //             borderColor: '#fff'
        //         },
        //         cellSize: 22,
        //         range: ['2023-01-01', '2023-03-11'],
        //         splitLine: true,
        //         dayLabel: {
        //             firstDay: 0,
        //             nameMap: dates
        //         },
        //         monthLabel: {
        //             show: false
        //         },
        //         yearLabel: {
        //             show: false
        //         },
        //         silent: {
        //             show: false
        //         }
        //     },
        //     series: {
        //         type: 'heatmap',
        //         coordinateSystem: 'calendar',
        //         data: data
        //     }
        // };
        // option && myChart.setOption(option);
        const heatmap = document.getElementById('heatmap');

        bookingsData.forEach((dayData, index) => {
            const dateLabel = document.createElement('div');
            dateLabel.className = 'date-label';
            dateLabel.textContent = dates[index];
            heatmap.appendChild(dateLabel);
        
            dayData.forEach(count => {
                const cell = document.createElement('div');
                cell.className = 'heatmap-cell';
                cell.style.backgroundColor = getColor(count);
                cell.setAttribute('data-count', count);
                heatmap.appendChild(cell);
            });
        });

        // Add a row for time labels
        // const timeLabels = document.createElement('div');
        // timeLabels.className = 'time-labels';

        // Add an empty cell for alignment
        const emptyCell = document.createElement('span');
        heatmap.appendChild(emptyCell);

        timeSlotMap = {
            0: "8:00",
            1: "8:55",
            2: "10:00",
            3: "10:55",
            4: "14:00",
            5: "14:55",
            6: "16:00",
            7: "16:55",
            8: "20:00",
            9: "20:55"
        }

        // Add time slots
        for (let i = 0; i < 10; i++) {
            const timeSlot = document.createElement('span');
            timeSlot.textContent = timeSlotMap[i];
            timeSlot.style.fontSize = '8px';
            heatmap.appendChild(timeSlot);
        }

        // heatmap.appendChild(timeLabels);

        function getColor(count) {
            if (count <= 0) return '#F5F5F5';
            if (count <= 1) return '#b0cbfc';
            if (count <= 3) return '#7c9edc';
            if (count <= 6) return '#4770bb';
            return '#13439b';
        }

        reports.separateData.forEach(report => {
            const reportItem = document.createElement('div');
            reportItem.classList.add('report-card');
            reportItem.innerHTML = `
                <div class="report-text">
                    <h3>${report.roomName}</h3>
                    <p>Weekly Usage: ${report.usage}%</p>
                </div>
            `;
            reportList.appendChild(reportItem);
        });
    }
    const loading_item = document.getElementById('loading-item');
    loading_item.style.display = 'none';
}