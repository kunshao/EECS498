// Get user pictures and display them.
function get_pictures () {
    log('Fetching your pictures ...');
    window.photo_count = 0;
    get_partial_picture_list(100, 0);
}

function get_partial_picture_list(limit, offset){
    log("Fetching a new page of photos...");
    query = 'me/photos?limit=' + limit + '&offset=' + offset;
    FB.api(query, function (response) {
        photo_list = response.data;

        if (photo_list.length > 0){
            window.photo_count += photo_list.length;

            save_photos(photo_list);
            get_partial_picture_list(limit, offset + limit)
        }
        else{
            document.getElementById("photo_list_length").innerHTML =
            window.photo_count + " photos retrieved."
        }

    })
}

function save_photos (list) {
    $.post(
        save_photo_url,
        JSON.stringify({photo_list : list, fb_owner_id : window.my_id}),
        function(server_response) {
            log(server_response);
        }
        );
}

