// Get user statuses and display them.
function get_posts () {
    log('Fetching your posts ...');
    window.post_count = 0;
    get_partial_post_list(100, 0);
}

function get_partial_post_list(limit, offset){
    log("Fetching new page...");
    query = 'me/posts?limit=' + limit + '&offset=' + offset;
    FB.api(query, function (response) {
        post_list = response.data;

        if (post_list.length > 0){
            window.post_count += post_list.length;
            // var post_list_ul = document.createElement("ul");
            // for (var i = 0; i < post_list.length; ++i){

            //     var status_li = document.createElement("li");
            //     status_li.innerHTML = post_list[i].message;
            //     if (post_list[i].comments){
            //         log("Making comment list...");
            //         status_li.appendChild(make_comment_list(post_list[i].comments));
            //     }
            //     else{
            //         log("No comment list...");
            //     }
            //     post_list_ul.appendChild(status_li);
            // }

            // document.getElementById("post_list_div").appendChild(post_list_ul)
            save_posts(post_list);
            get_partial_post_list(limit, offset + limit)
        }
        else{
            document.getElementById("post_list_length").innerHTML =
            window.post_count + " posts retrieved."
        }

    })
}
