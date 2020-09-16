
document.addEventListener('DOMContentLoaded', function () {
        const month = 'Janvier'
        var myChart = Highcharts.chart('graph', {
            chart: {
                type: 'column'
            },
                legend: {
                    bubbleLegend: {
                        enabled: true
                    }
                },
            title: {
                text: '<span class="title"> Mois de ' + month + ' </span>'
            },
            tooltip: {
                shared: true,
                headerFormat: '<span style="font-size: 15px"> Au {point.y} '+month+'</span><br/>',
                pointFormat: '<span style="color:{point.color}">\u25CF</span> {series.name}: <b>{point.y}</b><br/>'
            },
            xAxis: {
                categories: [1, 7, 14, 21, 28]
            },
            yAxis: {
                title: {
                    text: 'Nombre de propriÃ©taires'
                },
            },
            series: [{

                name: 'ContactÃ©s',
                data: [1, 7, 12, 19, 23],
                color : '#00b4b5',
            }, {
                name: 'A contactÃ©',
                data: [32, 28, 21, 20, 20],
                color : '#555555'
            }]
        });
    });