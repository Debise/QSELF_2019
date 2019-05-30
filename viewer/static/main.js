$(document).ready(function () {
    $('#nav-home-tab a').on('click', function (e) {
        e.preventDefault();
        $(this).tab('show');
    });

    $('#nav-profile-tab a').on('click', function (e) {
        e.preventDefault();
        $(this).tab('show');
    });

    $('#nav-contact-tab a').on('click', function (e) {
        e.preventDefault();
        $(this).tab('show');
    });
});

