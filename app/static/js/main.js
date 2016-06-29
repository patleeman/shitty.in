window.onload = function () {

    var app = new Vue({
      el: '#app',
      data: {
        message: 'Hello World!'
      }
    });
    console.log(app.message);
}
