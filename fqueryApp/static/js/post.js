// Get user statuses and display them.
function get_posts (id) {
    log('Fetching your posts ...');
    window.post_count = 0;
    get_partial_post_list(id, 100, 0);
}

function get_partial_post_list(id, limit, offset){
    log("Fetching new post page...");
    query = id + '/posts?limit=' + limit + '&offset=' + offset;
    FB.api(query, function (response) {
        post_list = response.data;

        if (post_list && post_list.length > 0){
            window.post_count += post_list.length;
            save_posts(id, post_list, true);
            get_partial_post_list(id, limit, offset + limit)
        }
        else{
            document.getElementById("post_list_length").innerHTML =
            window.post_count + " posts retrieved."
            ++num_types_retrieved_g;
            window.posts_ready = 1;
            save_posts(id, post_list, false);
        }
    })
}

function print_ready_signals(){
    log("window.posts_ready: " + window.posts_ready);
    log("window.statuses_ready: " + window.statuses_ready);
    log("window.pictures_ready: " + window.pictures_ready);
    log("window.links_ready: " + window.links_ready);
}

function save_posts(id, list, save){
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
            save_post_url,
            JSON.stringify({post_list : list, fb_owner_id : id}),
            function(server_response) {
                log(server_response);


                if (window.posts_ready == 1){
                    log("posts_ready");
                    window.posts_ready = 2;
                    print_ready_signals();
                }

                if (window.my_id != id && 
                    window.statuses_ready == 2 &&
                    window.pictures_ready == 2 &&
                    window.links_ready == 2 &&
                    window.posts_ready == 2){

                    sendQuery(window.query, window.content_type_flags, window.selected_friends);  

                    window.posts_ready = 3;  
                }
            }
          );
}
