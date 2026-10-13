function initInsightsCharts(chartLabels, chartScores, safeCount, suspiciousCount, highRiskCount) {
    const lineCtx = document.getElementById('lineChart').getContext('2d');
    new Chart(lineCtx, {
        type: 'line',
        data: {
            labels: chartLabels,
            datasets: [{
                label: 'Risk Score',
                data: chartScores,
                borderColor: '#00D4FF',
                backgroundColor: 'rgba(0, 212, 255, 0.1)',
                tension: 0.3,
                fill: true,
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true, max: 100, ticks: { color: '#94a3b8' } },
                x: { ticks: { color: '#94a3b8' } }
            },
            plugins: { legend: { labels: { color: '#F8FAFC' } } }
        }
    });

    const doughnutCtx = document.getElementById('doughnutChart').getContext('2d');
    new Chart(doughnutCtx, {
        type: 'doughnut',
        data: {
            labels: ['Safe', 'Suspicious', 'High Risk'],
            datasets: [{
                data: [safeCount, suspiciousCount, highRiskCount],
                backgroundColor: ['#4ade80', '#facc15', '#f87171'],
            }]
        },
        options: {
            plugins: { legend: { labels: { color: '#F8FAFC' } } }
        }
    });
}