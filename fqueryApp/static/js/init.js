window.fbAsyncInit = function() {
    FB.init({
        appId      : fb_app_id,
        status     : true,
        xfbml      : true
    });


    FB.Event.subscribe('auth.authResponseChange', function(response) {
        if (response.status === 'connected') {
            console.log("Logged in!");
            testAPI();

        } else {
            window.location = render_login_url;
            console.log("Not loggedin");
        }
    });
};

(function(d, s, id){
     var js, fjs = d.getElementsByTagName(s)[0];
     if (d.getElementById(id)) {return;}
     js = d.createElement(s); js.id = id;
     js.src = "//connect.facebook.net/en_US/all.js";
     fjs.parentNode.insertBefore(js, fjs);
 }(document, 'script', 'facebook-jssdk'));


function testAPI(){
    console.log('Welcome!  Fetching your information.... ');
    FB.api('/me', function(response) {
        console.log('Good to see you, ' + response.name + '.');
        window.my_id = response.id;
        window.my_name = response.name;
        console.log('ID: ', response.id);
    })

    // get_friend_list();
    get_statuses();
    get_pictures();
    get_links();
    get_posts();
}
