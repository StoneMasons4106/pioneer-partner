$('.like-button').click(function() {
    if($(this).hasClass('bi-heart-fill')) {
        $(this).removeClass('bi-heart-fill');
        $(this).addClass('bi-heart');
        var likes = $(this).closest('.like-column').find('.number-of-likes').text();
        likes = parseInt(likes) - 1;
        $(this).closest('.like-column').find('.number-of-likes').text(likes);
        var postId = $(this).closest('.card-footer').find('#post-id').val();
        var csrf = $('input[name="csrfmiddlewaretoken"]').attr("value");
        $.ajax({
            type: "POST",
            url: "/posts/remove_like/",
            data: {
                "postId": postId,
            },
            headers: {
                'X-CSRFToken': csrf,
            },
            contentType: "application/javascript",
            dataType: "json",
        });
    } else {
        $(this).removeClass('bi-heart');
        $(this).addClass('bi-heart-fill');
        var likes = $(this).closest('.like-column').find('.number-of-likes').text();
        likes = parseInt(likes) + 1;
        $(this).closest('.like-column').find('.number-of-likes').text(likes);
        var postId = $(this).closest('.card-footer').find('#post-id').val();
        var csrf = $('input[name="csrfmiddlewaretoken"]').attr("value");
        $.ajax({
            type: "POST",
            url: "/posts/add_like/",
            data: {
                "postId": postId,
            },
            headers: {
                'X-CSRFToken': csrf,
            },
            contentType: "application/javascript",
            dataType: "json",
        });
    }
});