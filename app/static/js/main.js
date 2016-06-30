
function get_api_data(){
    var api_data = null;
    $.ajax({
        url: "/api",
        datatype: "json",
        async: false,
        success: function(data){api_data = data;},
        });
    return api_data;
}

api_data = get_api_data();
console.log(api_data)
var app = new Vue({
  el: '#app',
  data: {
    weather_scores: api_data.weather_data.scores,
    weather_data: api_data.weather_data,
    transit: api_data.transit,
    transit_score: api_data.transit_score,
    overall: api_data.overall_score,
  }
});

var transit = Vue.extend({
  el: '#transit-breakdown',
  data: {
    transit: api_data.transit.scores
  }
});
