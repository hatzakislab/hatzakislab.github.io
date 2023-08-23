$(document).ready(function () {

    'use strict';

    var c, currentScrollTop = 0,
        navbar = $('nav'); // select the nav element

    $(window).scroll(function () {
        var a = $(window).scrollTop();
        var b = navbar.height();

        currentScrollTop = a;

        if (!($('.navbar-toggle').attr('aria-expanded') === "true")) {
            if (c < currentScrollTop && a > b + b) {
                navbar.addClass("scrollUp");
            } else if (c > currentScrollTop && !(a <= b)) {
                navbar.removeClass("scrollUp");
            }
            c = currentScrollTop;
        }
    });
});