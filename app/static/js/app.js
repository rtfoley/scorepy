$(document).ready(function () {
  window.setTimeout(function() {
      $(".alert-success").fadeTo(0, 0).fadeOut(500, function(){
          $(this).remove();
      });
  }, 2000);
});
