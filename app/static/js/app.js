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
    api: api_data
  }
});

var transit = Vue.extend({
  el: '#transit-breakdown',
  data: {
    api: api_data
  }
});
