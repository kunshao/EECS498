// Get user statuses and display them.
function get_statuses () {
    log('Fetching your statuses ...');
    window.status_count = 0;
    get_partial_status_list(100, 0);
}

function get_partial_status_list(limit, offset){
    log("Fetching new page...");
    query = 'me/statuses?limit=' + limit + '&offset=' + offset;
    FB.api(query, function (response) {
        status_list = response.data;

        if (status_list.length > 0){
            window.status_count += status_list.length;
            save_statuses(status_list);
            get_partial_status_list(limit, offset + limit)
        }
        else{
            document.getElementById("status_list_length").innerHTML =
            window.status_count + " statuses retrieved."
        }

    })
}

function save_statuses (status_list) {
    $.post(
            save_status_url,
            JSON.stringify({"status_list" : status_list, fb_owner_id : window.my_id}),
            function(server_response) {
            log(server_response);
            }
          );
}
