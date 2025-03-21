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
            <div id="main-chart" class="about"></div>
        `;
        reportList.appendChild(jointReport);
        const chartDom = document.getElementById('main-chart');
        const myChart = echarts.init(chartDom);
        var option;
        var data = [];

        function addDays(dateString, days) {
            const date = new Date(dateString);
            date.setDate(date.getDate() + days);
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            return `${year}-${month}-${day}`;
        }

        for (var i = 0; i < matrix.length; i++) {
            for (var j = 0; j < matrix[i].length; j++) {
                if (matrix[i][j] === 0) {
                    continue;
                }
                data.push([addDays('2023-01-01', j * 7 + i), matrix[i][j]]);
            }
        }

        option = {
            title: {
                top: 0,
                left: 'left',
                text: 'All Rooms Heatmap',
                textStyle: {
                    color: '#13439b'
                }
            },
            tooltip: {
                formatter: function (params) {
                    return String(params.value[1]);
                }
            },
            visualMap: {
                show: true,
                inRange: {
                    color: ['#b0cbfc', '#13439b']
                },
                type: 'piecewise',
                pieces: [
                    {min: 0, max: 1},
                    {min: 2, max: 3},
                    {min: 3, max: 6},
                    {min: 6},
                ],
                orient: 'horizontal',
                left: 'left',
                top: 30
            },
            calendar: {
                itemStyle: {
                    color: '#EBEDF0',
                    borderWidth: 3,
                    borderColor: '#fff'
                },
                cellSize: [20, 20],
                range: ['2023-01-01', '2023-03-11'],
                splitLine: true,
                dayLabel: {
                    firstDay: 0,
                    nameMap: dates
                },
                monthLabel: {
                    show: false
                },
                yearLabel: {
                    show: false
                },
                silent: {
                    show: false
                }
            },
            series: {
                type: 'heatmap',
                coordinateSystem: 'calendar',
                data: data
            }
        };
        option && myChart.setOption(option);

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
}