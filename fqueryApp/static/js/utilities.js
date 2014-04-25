//ideally I would like to have all of the fb event handlers done here

// Log to console
function log(msg) {
    console.log(msg);
}

function enableSearch(num_types){
    if (num_types_retrieved_g < num_types){
        var percentage = num_types_retrieved_g/num_types * 100; 
        document.getElementById("progressbar-inner").setAttribute("style", "width:"+ percentage.toString()+ "%;");
        setTimeout(function() {enableSearch(num_types);}, 100);
        return;
    }
    document.getElementById("progressbar-inner").setAttribute("style", "width:100%;");
    document.getElementById("loading").style.visibility = "hidden";
    document.getElementById("progressbar-outer").style.visibility = "hidden";
    document.getElementById("txtKeyword").disabled=false;
    document.getElementById("txtKeyword").focus();
    document.getElementById("btnMakeQuery").disabled=false;
}

function runmakeQuery(event){
    if (event.keyCode == 13) {
        makeQuery()
    }
}

function makeQuery(){
    var query     = document.getElementById("txtKeyword").value;
    var content_type_flags = get_content_type_flags();
    var selected_friends = get_selected_friend_list();
    for (var i = 0; i < selected_friends.length; i++) {

        log('selected: ' + selected_friends[i]);
    };
    for (var i = 0; selected_friends && i < selected_friends.length; i++) {
        log('makeQuery: '+ selected_friends[i]);
    };
    get_friends_data(selected_friends, content_type_flags, query);
}

function get_friends_data(selected_friends, content_type_flags, query){

    window.statuses_ready = 0;
    window.pictures_ready = 0;
    window.links_ready = 0;
    window.posts_ready = 0;

    document.getElementById("loading").style.visibility = "visible";
    document.getElementById("loading").innerHTML = "Retrieving";
    while (query_response_content_div.firstChild) {
        query_response_content_div.removeChild(query_response_content_div.firstChild);
    }
    if (!selected_friends) return;
    log("selected_friends size: ", selected_friends.length);
    window.query = query;
    window.content_type_flags = content_type_flags;
    window.selected_friends = selected_friends;

    if (selected_friends[0] == window.my_id){
        sendQuery(query, content_type_flags, selected_friends);
        return;
    }

    for (var i = 0; i < selected_friends.length; i++) {
        log("start retrieving data of " + selected_friends[i]);
        var id = selected_friends[i];
        
        get_statuses(id);
        get_pictures(id);
        get_links(id);
        get_posts(id);
        
    };
    // sendQuery(query, content_type_flags, selected_friends);
}

function sendQuery(query, content_type, selected_friends){
    log("entering sendQuery");
    $.post(
            make_query_url,
            JSON.stringify({
                owner_id : window.my_id, 
                query : document.getElementById("txtKeyword").value, 
                content_flags : content_type, 
                friend_list : selected_friends}),
            
            function(server_response) {
                document.getElementById("loading").innerHTML = "Done";
                content_list_obj = server_response.data;
                log(content_list_obj);

                var flagDict = getFlagDictionary();

                var content_list_div = document.createElement("div");
                for (content_type in content_list_obj){
                    log('parsing content type: ' + flagDict[content_type]);

                    var one_type_list = document.createElement("ul");

                    var one_type_div = document.createElement("div");

                    one_type_div.innerHTML = flagDict[content_type] + ": ";
                    content_list_div.appendChild(one_type_div);

                    content_list_div.appendChild(document.createElement("br"));

                    var content = content_list_obj[content_type];
                    for (key in content){
                        log("content: " + content);

                        var one_piece_content = document.createElement("li");
                        if (content[key].url) {
                            var hyperlink = document.createElement("a");
                            hyperlink.innerHTML = content[key].msg;
                            hyperlink.href = content[key].url;
                            hyperlink.target = "_blank";
                            one_piece_content.appendChild(hyperlink);
                        }
                        else {
                            one_piece_content.innerHTML = content[key].msg;
                        }

                        one_type_list.appendChild(one_piece_content);

                    }

                    content_list_div.appendChild(document.createElement("br"));
                    content_list_div.appendChild(one_type_list);      
                }
                var query_response_content_div = document.getElementById("query_response_content_div");
                // while (query_response_content_div.firstChild) {
                //     query_response_content_div.removeChild(query_response_content_div.firstChild);
                // }
                query_response_content_div.appendChild(content_list_div);
            })
}

function get_content_type_flags(){

    var content_type_flags = 0;
    var content_type_box = $('input[name="content_type_box"]');

    for (var i = 0; i < content_type_box.length; i++) {
        if (content_type_box[i].checked){
            content_type_flags = content_type_flags | content_type_box[i].value;
        }
    };
    return content_type_flags
}

function getFlagDictionary(){

    var flagDict = {}
    flagDict[1] = 'status';
    flagDict[1<<1] = 'post';
    flagDict[1<<2] = 'comment';
    flagDict[1<<3] = 'link';
    flagDict[1<<4] = 'photo';
    flagDict[1<<5] = 'note';
    flagDict[1<<6] = 'video';
    flagDict[1<<7] = 'question';
    flagDict[1<<8] = 'question option';

    return flagDict;
}
