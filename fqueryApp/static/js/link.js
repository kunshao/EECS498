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
            save_links(link_list);
            get_partial_link_list(id, limit, offset + limit)
        } else{
            document.getElementById("link_list_length").innerHTML = window.link_count + " links retrieved."
        }

    })
}

function save_links (list) {
    $.post(
        save_link_url,
        JSON.stringify({link_list : list, fb_owner_id : window.my_id}),
        function(server_response) {
            log(server_response);
        }
        );
}
