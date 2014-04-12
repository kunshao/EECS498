function make_comment_list(commment_list_obj){

    comment_list = commment_list_obj.data;

    var comment_list_ul = document.createElement("ul");
    for (var i = 0; i < comment_list.length; ++i){

        var comment_li = document.createElement("li");
        comment_li.innerHTML = comment_list[i].message;

        comment_list_ul.appendChild(comment_li);
    }
    return comment_list_ul;
}
