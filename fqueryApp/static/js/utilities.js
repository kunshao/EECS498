//ideally I would like to have all of the fb event handlers done here

// Log to console
function log(msg) {
    console.log(msg);
}

function runmakeQuery(event){
    if (event.keyCode == 13) {
        makeQuery()
    }
}

function makeQuery(){
    var query     = document.getElementById("txtKeyword").value;
    var content_type_flags = get_content_type_flags();
    document.getElementById("query_content_div").innerHTML = "You searched: " + query + " within " + content_type_flags;
    sendQuery(query, content_type_flags)
}

function sendQuery(query, content_type){
    $.getJSON(
            make_query_url,
            {query : query, content_flags : content_type},
            function(server_response) {

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

                    for (var i = 0; i < content_list_obj[content_type].length; ++i){

                        var one_piece_content = document.createElement("a");
                        var msg = content_list_obj[content_type][i].msg;

                        if (content_type == 16) {
                            //I absolutely do not like this, need a better way
                            var open_paran_loc = msg.lastIndexOf('(');
                            var desc = msg.substr(0, open_paran_loc);

                            ++open_paran_loc;
                            var close_paran_loc = msg.lastIndexOf(')');
                            var url = msg.substr(open_paran_loc, close_paran_loc-open_paran_loc);

                            one_piece_content.innerHTML = desc;
                            one_piece_content.href = url;
                            one_piece_content.target = "_blank";
                        }
                        else {
                            var one_piece_content = document.createElement("li");
                            one_piece_content.innerHTML = msg;
                        }

                        //one_piece_content.innerHTML = content_list_obj[content_type][i].msg;
                        one_type_list.appendChild(one_piece_content);

                    }

                    content_list_div.appendChild(one_type_list);
                }
                var query_response_content_div = document.getElementById("query_response_content_div");
                while (query_response_content_div.firstChild) {
                    query_response_content_div.removeChild(query_response_content_div.firstChild);
                }
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
