
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

initial_data = get_api_data();
console.log(initial_data);
var app = new Vue({
  el: '#app',
  data: {
    weather: initial_data.weather,
    transit: JSON.stringify(initial_data.transit)
  }
});

