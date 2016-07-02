var api_data = {};

var app = new Vue({
  el: '#app',
  data: {
    api: api_data
  }
});

var transit = Vue.extend({
  el: '#transit-breakdown',
  data: {
    api: api_data
  }
});

function get_api_data(){
    $.ajax({
        url: "/api",
        datatype: "json",
        async: true,
        success: function(data){
            app.api=data;
            transit.api=data;
            $("#weather-total").html(data.weather_scores.TOTAL);
            $("#transit-total").html(data.transit_score);
            stat();
        },
        });
}

//call it on ready
$(function(){ get_api_data(); });
