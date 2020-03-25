var initialize = function() {
  console.log('initalize called');
  $('input[name="text"]').on('keypress', function() {
    $('.has-error').hide();
  });
};
console.log('list.js loaded');
