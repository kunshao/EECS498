// Get user statuses and display them.
function get_notes(id) {
    log('Fetching your get_notes ...');
    window.note_count = 0;
    get_partial_note_list(id, 100, 0);
}

function get_partial_note_list(id, limit, offset){
    log("Fetching new note page...");
    query = id + '/notes?limit=' + limit + '&offset=' + offset;
    FB.api(query, function (response) {
        note_list = response.data;

        if (note_list && note_list.length > 0){
            window.note_count += note_list.length;
            save_notes(id, note_list);
            get_partial_note_list(id, limit, offset + limit)
        }
        else{
            document.getElementById("note_list_length").innerHTML =
            window.note_count + " notes retrieved."
            ++num_types_retrieved_g;
            if (window.my_id != id){
                sendQuery(window.query, window.content_type_flags, window.selected_friends);
            }
        }

    })
}

function save_notes (id, list) {
    $.post(
        save_note_url,
        JSON.stringify({note_list : list, fb_owner_id : id}),
        function(server_response) {
            log(server_response);
        }
        );
}
