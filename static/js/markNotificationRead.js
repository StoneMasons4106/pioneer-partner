$('.notification-button').click(function() {
    var notificationId = $(this).closest('div').find('.notification-id').val();
    var csrf = $('input[name="csrfmiddlewaretoken"]').attr("value");
    $.ajax({
        type: "POST",
        url: "/notifications/mark_read/" + notificationId + "/",
        data: {
            "notificationId": notificationId,
        },
        headers: {
            'X-CSRFToken': csrf,
        },
        contentType: "application/javascript",
        dataType: "json",
    });
  }
);