google.charts.load('current', {
    'packages': ['line', 'corechart']
});

let packetsObtainedData = [];
let errorsObtainedData = [];
let ramUsage = [];
let cpuUsage = [];

const URL = 'http://127.0.0.1:5000/system/stats';

function getPacketData() {
    var xhr = new XMLHttpRequest();

    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === 4) {
           let packetData = JSON.parse(this.responseText);
            packetsObtainedData.push([new Date(), packetData.packets.sent, packetData.packets.received]);
            errorsObtainedData.push([new Date(), packetData.packets.error]);
            ramUsage.push([new Date(), packetData.ram / 1e6]);
            cpuUsage.push([new Date(), packetData.cpu]);
            console.log(cpuUsage)
            drawChart();
        }
    });

    xhr.open("GET", URL);
    xhr.setRequestHeader("content-type", "application/json");
    xhr.send();
}

getPacketData();
setInterval(function(){
    getPacketData()}, 5000);

function drawChart() {
    var packetsChartDiv = document.getElementById('packets_chart_div');
    var packetsData = new google.visualization.DataTable();
    packetsData.addColumn('date', 'Date');
    packetsData.addColumn('number', "Sent packets");
    packetsData.addColumn('number', "Received packets");

    packetsData.addRows(packetsObtainedData);

    var packetsOptions = {
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


    function drawPacketsChart() {
        var materialChart = new google.charts.Line(packetsChartDiv);
        materialChart.draw(packetsData, packetsOptions);
    }

    drawPacketsChart();
    
    var errorsChartDiv = document.getElementById('errors_chart_div');
    var errorsData = new google.visualization.DataTable();
    errorsData.addColumn('date', 'Date');
    errorsData.addColumn('number', "Errors");

    errorsData.addRows(errorsObtainedData);

    var errorsOptions = {
        chart: {
            title: 'Erros'
        },
        width: 900,
        height: 500,
        series: {
            // Gives each series an axis name that matches the Y-axis below.
            0: {
                axis: 'Packets',
                color: 'red'
            },
            1: {
                axis: 'Date'
            }
        },
        axes: {
            // Adds labels to each axis; they don't have to match the axis names.
            y: {
                Packets: {
                    label: 'Errors'
                }
            }
        }
    };
    
    function drawErrorsChart() {
        var materialChart = new google.charts.Line(errorsChartDiv);
        materialChart.draw(errorsData, errorsOptions);
    }

    drawErrorsChart();
    
    var ramChartDiv = document.getElementById('ram_chart_div');
    var ramData = new google.visualization.DataTable();
    ramData.addColumn('date', 'Date');
    ramData.addColumn('number', "Ram Usage");

    ramData.addRows(ramUsage);

    var ramOptions = {
        chart: {
            title: 'Ram Usage'
        },
        width: 900,
        height: 500,
        series: {
            // Gives each series an axis name that matches the Y-axis below.
            0: {
                axis: 'Packets',
                color: 'purple'
            },
            1: {
                axis: 'Date'
            }
        },
        axes: {
            // Adds labels to each axis; they don't have to match the axis names.
            y: {
                Packets: {
                    label: 'Mb'
                }
            }
        }
    };
    
    function drawRamChart() {
        var materialChart = new google.charts.Line(ramChartDiv);
        materialChart.draw(ramData, ramOptions);
    }

    drawRamChart();
    
    var cpuChartDiv = document.getElementById('cpu_chart_div');
    var cpuData = new google.visualization.DataTable();
    cpuData.addColumn('date', 'Date');
    cpuData.addColumn('number', "CPU Usage");

    cpuData.addRows(cpuUsage);

    var cpuOptions = {
        chart: {
            title: 'CPU Usage'
        },
        width: 900,
        height: 500,
        series: {
            // Gives each series an axis name that matches the Y-axis below.
            0: {
                axis: 'Packets',
                color: 'green'
            },
            1: {
                axis: 'Date'
            }
        },
        axes: {
            // Adds labels to each axis; they don't have to match the axis names.
            y: {
                Packets: {
                    label: 'Percentage'
                }
            }
        }
    };
    
    function drawCpuChart() {
        var materialChart = new google.charts.Line(cpuChartDiv);
        materialChart.draw(cpuData, cpuOptions);
    }

    drawCpuChart();
}
