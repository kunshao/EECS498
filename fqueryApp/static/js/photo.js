// Get user pictures and display them.
function get_pictures () {
    log('Fetching your pictures ...');
    window.photo_count = 0;
    get_partial_picture_list(100, 0);
}

function get_partial_picture_list(limit, offset){
    log("Fetching a new page of photos...");
    query = 'me/photos?limit=' + limit + '&offset=' + offset;
    FB.api(query, function (response) {
        photo_list = response.data;

        if (photo_list.length > 0){
            window.photo_count += photo_list.length;
            // var photo_list_ul = document.createElement("ul");
            // for (var i = 0; i < photo_list.length; ++i){

            //     var photo_li = document.createElement("li");
            //     photo_li.innerHTML = photo_list[i].name;

            //     // Attach photo
            //     var photo_img = document.createElement("img");
            //     photo_img.src = photo_list[i].source;
            //     photo_img.width = photo_list[i].width;
            //     photo_img.height = photo_list[i].height;

            //     photo_list_ul.appendChild(photo_img);

            //     // Attach comments
            //     if (photo_list[i].comments){
            //         log("Making comment list...");
            //         photo_li.appendChild(make_comment_list(photo_list[i].comments));
            //     }

            // photo_list_ul.appendChild(photo_li);
            // document.getElementById("photo_list_div").appendChild(photo_list_ul)
            get_partial_picture_list(limit, offset + limit)
        }
        else{
            document.getElementById("photo_list_length").innerHTML =
            window.photo_count + " photos retrieved."
        }

    })
}
