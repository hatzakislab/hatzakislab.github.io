$("document").ready(function () {
    $('#bs-example-navbar-collapse-1 ul li a').on('click', function () {
        $('.navbar-toggle:visible').click();
    });
});