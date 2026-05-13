document.addEventListener("DOMContentLoaded", () => {

    const ctx = document.getElementById('graficaTemporadas');

    if (ctx && window.datosGrafica) {

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: window.datosGrafica.labels,
                datasets: [{
                    label: 'Ventas por temporada',
                    data: window.datosGrafica.data,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: {
                            color: '#ffffff'
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: '#ffffff'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: '#ffffff',
                            precision: 0
                        }
                    }
                }
            }
        });

    }

});