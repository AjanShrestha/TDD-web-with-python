window.Superlists = {};
window.Superlists.initialize = function () {
  $('input[name="text"]').on('keypress', function() {
    $('.has-error').hide();
  });
};
// Our initialize function name is too generic—what if we include 
// some third-party JavaScript tool later that also defines a 
// function called initialize? 