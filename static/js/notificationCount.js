$(document).ready(function() {
    var items = $('.notification-item');
    $('.badge-number').html(items.length);
    $('.notification-statement').html(items.length);
});