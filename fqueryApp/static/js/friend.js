function get_friend_list(){
    log('Fetching your friend list...');
    FB.api('/me/friends', function(response){
            log("Total of " + response.data.length + " friends.");

            // Display friend list.
            var friend_list_li = document.createElement("ul");
            for (var i = 0; i < response.data.length; ++i){
            // log("")
            console.log("Processing " + response.data[i].name);
            var one_friend_element = document.createElement("li");
            one_friend_element.innerHTML =  response.data[i].id + " " +
            response.data[i].name;
            friend_list_li.appendChild(one_friend_element);
            }

            document.getElementById("friend_list_div").appendChild(friend_list_li)

            });
}
