// guide for user to trully input right data
$(function() {
    var text;
    $('#user').keyup(function() {
        text = $('#user').val();
        if (text.length <= 5 || text.length > 30 && /^[a-zA-Z][a-zA-Z0-9]/.test(
            text) == false) {

            $('.warnning.user').text(
            'user should be 5<user<30 , not start with numbers');
            $('#username').removeClass('has-success has-feedback');
        }

        else {
            $('#username').addClass('has-success has-feedback');
            $('.warnning.user').text(' ');
        }
    });

    $('#email').keyup(function() {
        if (/[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$/.test(
            $('#email').val()) == false) {

            $('.warnning.email').text('type valid email');
            $('#mail').removeClass('has-success has-feedback');

        }
        else {

            $('.warnning.email').text(' ');
            $('#mail').addClass('has-success has-feedback');

        }
    });

    $('#password').keyup(function() {
        var password = $('#password').val();
        if (password.length <= 8) {

            $('.warnning.password').text('password should be longer than 8');
            $('#pass').removeClass('has-success has-feedback');


        }
        else {
            $('.warnning.password').text(' ');
            $('#pass').addClass('has-success has-feedback');

        }
    });

    $('#verify, #password').keyup(function() {

        var password = $('#password').val();
        var verify = $('#verify').val();

        if (password == verify && verify) {
            $('.warnning.verify').text(' ');
            $('#veri').addClass('has-success has-feedback');

        }
        else {
            $('.warnning.verify').text('password missmatch');
            $('#veri').removeClass('has-success has-feedback');

        }
    });
// enable and disable submit button if data is truly entered
    $('*').keyup(function() {

        if ($('#veri').hasClass('has-success') &&
            $('#pass').hasClass('has-success') &&
            $('#mail').hasClass('has-success') &&
            $('#username').hasClass('has-success') == true) {

            $('#submit').removeAttr('disabled');

        }
        else {

            $('#submit').attr('disabled', true);
        }

    });
});
