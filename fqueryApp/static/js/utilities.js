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
    flagDict[1<<1] = 'comment';
    flagDict[1<<2] = 'link';
    flagDict[1<<3] = 'photo';
    flagDict[1<<4] = 'note';
    flagDict[1<<5] = 'post';
    flagDict[1<<6] = 'video';
    flagDict[1<<7] = 'question';
    flagDict[1<<8] = 'question option';

    return flagDict;
}
