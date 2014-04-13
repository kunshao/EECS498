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
            // var status_list_ul = document.createElement("ul");
            // for (var i = 0; i < status_list.length; ++i){

            //     var status_li = document.createElement("li");
            //     status_li.innerHTML = status_list[i].message;
            //     if (status_list[i].comments){
            //         log("Making comment list...");
            //         status_li.appendChild(make_comment_list(status_list[i].comments));
            //     }
            //     else{
            //         log("No comment list...");
            //     }
            //     status_list_ul.appendChild(status_li);
            // }

            // document.getElementById("status_list_div").appendChild(status_list_ul)
            save_statuses(status_list);
            get_partial_status_list(limit, offset + limit)
        }
        else{
            document.getElementById("status_list_length").innerHTML =
            window.status_count + " statuses retrieved."
        }

    })
}
