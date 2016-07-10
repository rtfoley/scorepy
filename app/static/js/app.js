$(document).ready(function () {
  window.setTimeout(function() {
      $(".alert-success").fadeTo(1000, 0).fadeOut(1000, function(){
          $(this).remove();
      });
  }, 3000);
});
