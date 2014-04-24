// Get user links and display them.
function get_links (id) {
    log('Fetching your statuses ...');
    window.link_count = 0;
    get_partial_link_list(id, 100, 0);
}
function get_partial_link_list(id, limit, offset){
    log("Fetching new page...");
    query = id + '/links?limit=' + limit + '&offset=' + offset;
    FB.api(query, function (response) {
        link_list = response.data;

        if (link_list && link_list.length > 0){
            window.link_count += link_list.length;
            save_links(id, link_list, true);
            get_partial_link_list(id, limit, offset + limit)
        } else{
            document.getElementById("link_list_length").innerHTML = window.link_count + " links retrieved."
            ++num_types_retrieved_g;
            window.links_ready = 1;
            save_links(id, link_list, false);
        }

    })
}

function save_links (id, list, save) {
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
        save_link_url,
        JSON.stringify({link_list : list, fb_owner_id : id, 
            retriever_id: window.my_id}),
        function(server_response) {
            log(server_response);

            if (window.links_ready == 1){
                window.links_ready = 2;
                log("links_ready");
                print_ready_signals();
            }

            if (window.my_id != id && 
                window.statuses_ready == 2 &&
                window.pictures_ready == 2 &&
                window.links_ready == 2 &&
                window.posts_ready == 2){

                sendQuery(window.query, window.content_type_flags, window.selected_friends);    


                window.links_ready = 3;
            }
        }
        );
}
