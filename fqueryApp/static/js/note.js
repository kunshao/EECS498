// Get user statuses and display them.
function get_notes() {
    log('Fetching your get_notes ...');
    window.note_count = 0;
    get_partial_note_list(100, 0);
}

function get_partial_note_list(limit, offset){
    log("Fetching new note page...");
    query = 'me/notes?limit=' + limit + '&offset=' + offset;
    FB.api(query, function (response) {
        note_list = response.data;

        if (note_list.length > 0){
            window.note_count += note_list.length;
            save_notes(note_list);
            get_partial_note_list(limit, offset + limit)
        }
        else{
            document.getElementById("note_list_length").innerHTML =
            window.note_count + " notes retrieved."
        }

    })
}

function save_notes (list) {
    $.post(
        save_note_url,
        JSON.stringify(list),
        function(server_response) {
            log(server_response);
        }
        );
}
