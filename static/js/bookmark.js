$('.bookmark-button').click(function() {
    if($(this).hasClass('bi-bookmark-fill')) {
        $(this).removeClass('bi-bookmark-fill');
        $(this).addClass('bi-bookmark');
        var postId = $(this).closest('.card-footer').find('#post-id').val();
        var csrf = $('input[name="csrfmiddlewaretoken"]').attr("value");
        $.ajax({
            type: "POST",
            url: "/posts/remove_bookmark/",
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
        $(this).removeClass('bi-bookmark');
        $(this).addClass('bi-bookmark-fill');
        var postId = $(this).closest('.card-footer').find('#post-id').val();
        var csrf = $('input[name="csrfmiddlewaretoken"]').attr("value");
        $.ajax({
            type: "POST",
            url: "/posts/add_bookmark/",
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