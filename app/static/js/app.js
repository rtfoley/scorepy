$(document).ready(function () {
  window.setTimeout(function() {
      $(".alert-success").fadeTo(1000, 0).fadeOut(1000, function(){
          $(this).remove();
      });
  }, 2000);

  window.setTimeout(function() {
      $(".alert-auto-dismiss").fadeTo(1000, 0).fadeOut(1000, function(){
          $(this).remove();
      });
  }, 5000);
});
