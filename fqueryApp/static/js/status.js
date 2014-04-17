// Get user statuses and display them.
function get_statuses (id) {
    log('Fetching ' + id + ' statuses ...');
    window.status_count = 0;
    get_partial_status_list(id, 100, 0);
}

function get_partial_status_list(id, limit, offset){
    log("Fetching new page...");
    
    query = id + '/statuses?limit=' + limit + '&offset=' + offset;
    log(query)
    FB.api(query, function (response) {
        status_list = response.data;

        if (status_list && status_list.length > 0){
            window.status_count += status_list.length;
            save_statuses(id, status_list);
            get_partial_status_list(id, limit, offset + limit)
        }
        else{
            document.getElementById("status_list_length").innerHTML =
            window.status_count + " statuses retrieved."
        }

    })
}

function save_statuses (id, status_list) {
    $.post(
            save_status_url,
            JSON.stringify({"status_list" : status_list, fb_owner_id : id}),
            function(server_response) {
            log(server_response);
            }
          );
}
