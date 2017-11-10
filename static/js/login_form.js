$(function() {

  $('#login-form-link').click(function(e) {
    $("#login-form").delay(100).fadeIn(100);
    $("#register-form").fadeOut(100);
    $('#register-form-link').removeClass('active');
    $(this).addClass('active');
    e.preventDefault();
  });
  $('#register-form-link').click(function(e) {
    $("#register-form").delay(100).fadeIn(100);
    $("#login-form").fadeOut(100);
    $('#login-form-link').removeClass('active');
    $(this).addClass('active');
    e.preventDefault();
  });
  // $('#register-form').submit(function() {
  //   // var success = $('<div class="alert alert-success alert-dismissable fade in" />');
  //   var error = $('<div class="alert alert-danger alert-dismissable fade in" />');
  //   // $('#register-form').append(success)
  //   // TODO: Both are same password thing
  //   $.ajax({
  //     url: '/sign_up',
  //     data: $('form').serialize(),
  //     type: 'POST'
  //   }).done((request) => {
  //     if(request.error) {
  //       $register-form.append(error);
  //       return false;
  //     }
  //   });
  // });

});
