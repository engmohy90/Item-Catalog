// google login
var googleUser = {};
var startApp = function() {
    gapi.load('auth2', function() {
        auth2 = gapi.auth2.init({
            client_id: '122663021563-qgegpul8s3rjflmk3im5grfmj29f2i78' +
            '.apps.googleusercontent.com',
            cookiepolicy: 'single_host_origin',
        });
        auth2.attachClickHandler(document.getElementById('customBtn'), {},
            function(googleUser) {
                var id_token = googleUser.getAuthResponse().id_token;
                $.ajax('/gconnect?rand=' + rand, {
                    method: 'POST',
                    data: id_token,
                    contentType: 'application/octet-stream; charset=utf-8',
                    success: function(result) {
                        if (result == 'logedin') {
                            location.href = '/catalog';
                        }
                        else {
                            location.reload()
                        }
                    }
                }).fail(function(result){
                    alert(result["responseText"]);
                    location.reload();
                });

            },
            function(error) {
                alert(JSON.stringify(error, undefined, 2));
            }
        );
    });
};

// face booooooooooooook
window.fbAsyncInit = function() {
    FB.init({
        appId: '1466381860048602',
        cookie: true,
        xfbml: true,
        version: 'v2.8'
    });
    FB.AppEvents.logPageView();
};

(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {return;}
    js = d.createElement(s); js.id = id;
    js.src = '//connect.facebook.net/en_US/sdk.js';
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

function checkLoginState() {
    FB.getLoginStatus(function(response) {
        if (response.status === 'connected') {
            var accessToken = response.authResponse.accessToken;
            $.ajax('/facelogin?rand=' + rand, {
                method: 'POST',
                data: accessToken,
                contentType: 'application/octet-stream; charset=utf-8',
                success: function(result) {
                    if (result == 'logedin') {
                        location.href = '/catalog';

                    }

                }

            });
        }
    });
}
