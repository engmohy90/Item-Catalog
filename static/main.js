// hide and preview data up on loged in or not
$(function() {
    if (userName == 'None') {
        $('.logedin').hide();
    }

    else {
        $('.logedout').hide();
        $('#myNavbar').prepend("<ul class='nav navbar-nav navbar-right'" +
        " id='wellcome' ><li><img id='profilelogo' src='" + photoUrl +
        "'><a href='/catalog/" + user_id + "/profile'>wellcome (" +
        userName + ')</a></li></ul>');
    }
// hiding flash after few seconds
    $('.flashes').fadeOut(9000);

});
