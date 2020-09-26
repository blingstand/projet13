//123
let CreateChart = function(container, datas){
    if ([typeof(container),typeof(datas)] == ['string', 'object']){
        console.log('graph.js : réception de données au mauvais format')
    }else{
        console.log('graph.js : réception de données au bon format')}
    var myChart = Highcharts.chart(container, {
        chart: {
            type: 'column', 
            margin: [50,10,0,10], 
            backgroundColor: "#e4e6e7"
        },
        legend: {
            bubbleLegend: {
                enabled: true
            }
        },
        title: {

            text: '<span class="title">Propriétaire devant encore stériliser</span>'
        },
        tooltip: {
            shared: true,
            headerFormat: '<span style="font-size: 15px"> Au {point.x}</span><br/>',
            pointFormat: '<span style="color:{point.color}">\u25CF</span> {series.name}: <b>{point.y}</b><br/>'
        },
        xAxis: {
            height: '80%',
            labels: {
                formatter: function() {
                    return "<span class='text-bold'>" + this.value+"</span>";
                }
            },
            resize: {
                enabled: true
            },
            categories: datas['date']
        },
        yAxis: {
          height: '80%',

          resize: {
            enabled: true
            },
            title: {
                text: 'Nombre de propriétaires'
        },
    },
    series: [{

        name: 'Contactés',
        data: datas['contacted'],
        color : '#00b4b5',
    }, {
        name: 'A contacté',
        data: datas['to contact'],
        color : '#555555'
    }]
    });
    return myChart
}