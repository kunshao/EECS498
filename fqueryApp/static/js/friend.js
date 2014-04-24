function get_friend_list(){
    
    log('Fetching your friend list...');
    FB.api('/me/friends', function(response){
        log("Total of " + response.data.length + " friends.");

            // Display friend list.
            // var friend_list_li = document.createElement("ul");
            // for (var i = 0; i < response.data.length; ++i){
            // // log("")
                
            //     var one_friend_element = document.createElement("li");
            //     one_friend_element.innerHTML =  response.data[i].id + " " +response.data[i].name;
            //     friend_list_li.appendChild(one_friend_element);
            // }

            // document.getElementById("friend_list_div").appendChild(friend_list_li)
            create_friend_select_list(sortByKey(response.data, 'name'));

        });
}

function create_friend_select_list(friend_list){
    
    for (var i = 0; i < friend_list.length; i++) {

        // console.log("Processing " + friend_list[i].name);
        var friend_option = document.createElement("option");
        friend_option.setAttribute("value", friend_list[i].id);
        friend_option.text = friend_list[i].name;
        document.getElementById("select_friends").appendChild(friend_option);
    };
}

function get_selected_friend_list(){
    var selected_friend_list = $('#select_friends').val();
    if (!selected_friend_list){
        selected_friend_list = new Array();
        selected_friend_list.push(window.my_id);
    };
    

    log('about to return from get_selected_friend_list');
    return selected_friend_list;
}

function sortByKey(array, key) {
    return array.sort(function(a, b) {
        var x = a[key]; var y = b[key];
        return ((x < y) ? -1 : ((x > y) ? 1 : 0));
    });
}