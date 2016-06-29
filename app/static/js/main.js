
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
var app = new Vue({
  el: '#app',
  data: {
    weather: api_data.weather,
    transit: api_data.transit.scores
  }
});

var transit = Vue.extend({
  el: '#transit-breakdown',
  data: {
    transit: api_data.transit.scores
  }
})