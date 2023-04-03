$('.comment-button').click(function() {
    var existing_comment_form = $('form#comment-form');
    if (existing_comment_form.length != 0) {
        //pass
    } else {
        var postId = $(this).closest('.card-footer').find('#post-id').val();
        var csrf = $('input[name="csrfmiddlewaretoken"]').attr("value");
        $(this).closest('.card-footer').html('<form class="row g-3" action="/posts/add_comment/" method="post" id="comment-form"><input type="hidden" name="csrfmiddlewaretoken" value="'+ csrf +'"><input type="hidden" id="original-post-id" name="original-post-id" value="'+ postId +'"><textarea required form="comment-form" name="comment-text" class="form-control" placeholder="Write something..." style="height: 100px"></textarea><div class="text-center"><button type="submit" class="btn btn-primary"><i class="bi bi-pencil-square"></i> Post</button></div></form>');
    }
});