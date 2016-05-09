(function($){
  $(function(){

    $('.button-collapse').sideNav();
    $('select').material_select();
    $('.datepicker').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 15 // Creates a dropdown of 15 years to control year
  });

  $('.modal-trigger').leanModal();

  0

  }); // end of document ready
})(jQuery); // end of jQuery name space