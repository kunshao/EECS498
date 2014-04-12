// Get user links and display them.
function get_links () {
    log('Fetching your statuses ...');
    window.link_count = 0;
    get_partial_link_list(100, 0);
}
function get_partial_link_list(limit, offset){
    log("Fetching new page...");
    query = 'me/links?limit=' + limit + '&offset=' + offset;
    FB.api(query, function (response) {
            link_list = response.data;

            if (link_list.length > 0){
            window.link_count += link_list.length;
            save_links(link_list);
            get_partial_link_list(limit, offset + limit)
            }
            else{
            document.getElementById("link_list_length").innerHTML = window.link_count + " links retrieved."
            }

            })
}


function save_links (list) {
    $.post(
            "{% url 'fqueryApp:save_links' %}",
            JSON.stringify(list),
            function(server_response) {
            log(server_response);
            }
          );
}
