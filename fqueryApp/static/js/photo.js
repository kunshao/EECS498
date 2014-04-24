// Get user pictures and display them.
function get_pictures (id) {
    log('Fetching your pictures ...');
    window.photo_count = 0;
    get_partial_picture_list(id, 100, 0);
}

function get_partial_picture_list(id, limit, offset){
    log("Fetching a new page of photos...");
    query = 'me/photos?limit=' + limit + '&offset=' + offset;
    FB.api(query, function (response) {
        photo_list = response.data;

        if (photo_list && photo_list.length > 0){
            window.photo_count += photo_list.length;

            save_photos(id, photo_list, true);
            get_partial_picture_list(id, limit, offset + limit)
        }
        else{
            document.getElementById("photo_list_length").innerHTML =
            window.photo_count + " photos retrieved."
            ++num_types_retrieved_g;
            window.pictures_ready = 1;
            save_photos(id, photo_list, false);
        }

    })
}

function save_photos (id, list,save) {
    if (!save){
        if (window.statuses_ready == 1){
            window.statuses_ready = 2;
            log("statuses_ready");
            print_ready_signals();
        }

        log(window.my_id != id);

        if (window.my_id != id && 
            window.statuses_ready == 2 &&
            window.pictures_ready == 2 &&
            window.links_ready == 2 &&
            window.posts_ready == 2){

            sendQuery(window.query, window.content_type_flags, window.selected_friends);    

            window.statuses_ready = 3;

        }
        return;
    }
    $.post(
        save_photo_url,
        JSON.stringify({photo_list : list, fb_owner_id : id}),
        function(server_response) {
            log(server_response);

            if (window.pictures_ready == 1){
                window.pictures_ready = 2;
                log("pictures_ready");
                print_ready_signals();
            }

            if (window.my_id != id && 
                window.statuses_ready == 2 &&
                window.pictures_ready == 2 &&
                window.links_ready == 2 &&
                window.posts_ready == 2){

                sendQuery(window.query, window.content_type_flags, window.selected_friends);  

                window.pictures_ready = 3;  
            }
        }
        );
}

