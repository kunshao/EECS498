// Get user statuses and display them.
function get_statuses (id) {
    log('Fetching ' + id + ' statuses ...');
    window.status_count = 0;
    get_partial_status_list(id, 100, 0);
    log('exiting get_statuses');
}

function get_partial_status_list(id, limit, offset){
    log("Fetching new page...");
    
    query = id + '/statuses?limit=' + limit + '&offset=' + offset;
    log(query)
    FB.api(query, function (response) {
        status_list = response.data;

        if (status_list && status_list.length > 0){
            window.status_count += status_list.length;
            save_statuses(id, status_list, true);
            get_partial_status_list(id, limit, offset + limit)
        }
        else{
            document.getElementById("status_list_length").innerHTML =
            window.status_count + " statuses retrieved."
            ++num_types_retrieved_g;
            window.statuses_ready = 1;
            save_statuses(id, status_list, false);
        }

    })
}

function save_statuses (id, status_list, save) {
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
            save_status_url,
            JSON.stringify({"status_list" : status_list, fb_owner_id : id, 
                retriever_id: window.my_id}),
            function(server_response) {
                log(server_response);

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



            }
          );
}
