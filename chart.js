/**
 * Created by Student on 22/12/2016.
 */
var Markit={};

//Define TimeseriesService
//First argument is symbol (string) for the quote.
//second argument is de duration for how many days of history to retrieve

Markit.TimeseriesService = function (symbol, duration) {
    this.symbol = symbol;
    this.duration = duration;
    this.PlotChart();
}

Markit.TimeseriesService.prototype.PlotChart = function () {
    //Make JSON request for timeseries data
    $.ajax({
        beforeSend:function () {
            $("#chartStockContainer").text("Loading chart ....");
        },
        data: {
            symbol: this.symbol,
            duration : this.duration
        },
        url: "http://dev.markitondemand.com/Api/Timeseries/jsonp",
        dataType: "jsonp",
        context : this,
        success: function (json) {
            //Catch errors
            if(!json.Data||json.Message){
                console.error("Error : ",json.Message);
                return;
            }
            this.BuildDataAndChart(json);
        },
        error:function () {
            alert("Couldn't generate chart")
        }
    });
};

Markit.TimeseriesService.prototype.BuildDataAndChart = function (json) {
    var dateDs = json.Data.SeriesDates,
        closeDs = json.Data.Series.close.values,
        openDs= json.Data.Series.open.values,
        closeDSLen = closeDs.length,
        irregularIntervalDs = [];

    /**
     * Build array of arrays of data & price values
     * Market data is inherently irregular and Highcharts doesnt
     * really like irregularity (for axis intervals, anyway)
     */

    for(var i = 0 ; i<closeDSLen; i++){
        var dat = new Date(dateDs[i]);
        var dateIn = Date.UTC(dat.getFullYear(),dat.getMonth(),dat.getDate());
        var val = closeDs[i];
        irregularIntervalDs.push([dateIn,val]);
    }

    // set dataset and chart label
    this.oChartOptions.series[0].data = irregularIntervalDs;
    this.oChartOptions.title.text = "Price History of "  + json.data.Name + "(1 year)";

//    init chart
    new Highcharts.Chart(this.oChartOptions)
};

//Define the HighCharts options
Markit.TimeseriesService.prototype.oChartoptions={
    chart:{
        renderTo : 'chartStockContainer'
    },
    title:{},
    subtitle:{
        text:"Source : Thomas Reuters Datascope / Markit on Demand"
    },
    xAxis: {
        type : "datetime"
    },
    yAxis : [{
        //left y axis
        title: {
            text: null
        },
        labels: {
            align: "left",
            x: 3,
            y: 16,
            formatter: function () {
                return Highcharts.numberFormat(this.value, 0);
            }
        },
        showFirstLabel: false
    },{
        //right axis
        linkedTo : 0,
        gridLineWidth:0,
        opposite: true,
        title : {
            text: null
        },
        labels: {
            align:"right",
            x: -3,
            y : 16,
            formatter : function () {
                return Highcharts.numberFormat(this.value,0);
            }
        },
        showFirstLabel : false
    }],
    tooltip : {
        shared: true,
        crosshairs:true
    },
    plotOptions : {
        series : {
            marker : {
                lineWidth : 1
            }
        }
    },
    series : [{
        name : "Close Price",
        lineWidth : 2,
        marker :{
            radius : 0
        }
    }]
};

new Markit.TimeseriesService("GOOG",365);

