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
            save_posts(id, post_list);
            get_partial_post_list(id, limit, offset + limit)
        }
        else{
            document.getElementById("post_list_length").innerHTML =
            window.post_count + " posts retrieved."
            ++num_types_retrieved_g;
        }

    })
}

function save_posts(id, list){
    $.post(
            save_post_url,
            JSON.stringify({post_list : list, fb_owner_id : id}),
            function(server_response) {
            log(server_response);
            }
          );
}
