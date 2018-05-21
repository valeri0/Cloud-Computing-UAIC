google.charts.load('current', {
    'packages': ['line', 'corechart']
});

let obtainedData = [];
const URL = 'http://127.0.0.1:5000/system/stats';

function getPacketData() {
    var xhr = new XMLHttpRequest();

    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === 4) {
           let packetData = JSON.parse(this.responseText);
            obtainedData.push([new Date(), packetData.packets.sent, packetData.packets.received]);
            console.log(obtainedData)
            drawChart();
        }
    });

    xhr.open("GET", URL);
    xhr.setRequestHeader("content-type", "application/json");
    xhr.send();
}

getPacketData();
setInterval(function(){
    getPacketData()}, 30000);

function drawChart() {
    var chartDiv = document.getElementById('chart_div');
    var data = new google.visualization.DataTable();
    data.addColumn('date', 'Date');
    data.addColumn('number', "Sent packets");
    data.addColumn('number', "Received packets");

    data.addRows(obtainedData);

    var materialOptions = {
        chart: {
            title: 'Network Packets'
        },
        width: 900,
        height: 500,
        series: {
            // Gives each series an axis name that matches the Y-axis below.
            0: {
                axis: 'Packets'
            },
            1: {
                axis: 'Date'
            }
        },
        axes: {
            // Adds labels to each axis; they don't have to match the axis names.
            y: {
                Packets: {
                    label: 'Number of packets'
                }
            }
        }
    };


    function drawMaterialChart() {
        var materialChart = new google.charts.Line(chartDiv);
        materialChart.draw(data, materialOptions);
    }

    drawMaterialChart();
}
