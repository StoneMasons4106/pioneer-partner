$('#add-house-button').click(function() {
    var form = $('#add-house-number-form').serializeArray();
    var csrf = form[0]["value"];
    var territory_id = form[2]["value"];
    var street_id = form[3]["value"];
    if (form[1]["value"]) {
        $.ajax({
            type: "POST",
            url: "/service/my_territory/" + territory_id + "/nh_records/" + street_id + "/",
            data: {
               "form": form,
            },
            headers: {
                'X-CSRFToken': csrf,
            },
            contentType: "application/javascript",
            dataType: "json",
            success: function(data) {
                var last_house = $('.houses').children('.house:last');
                if (last_house.length != 0) {
                    var class_list = last_house.prop('className').split(' ');
                    var last_house_class_id = class_list.at(-1);
                    var house_id = parseInt(last_house_class_id.split('-')[1]) + 1;
                    $('.houses').append('<div class="row house house-'+house_id+'"><!-- Sales Card --><div class="col"><div class="card info-card invite-card"><div class="card-body invite-card-body"><div class="d-flex align-items-center"><div class="card-icon rounded-circle d-flex align-items-center justify-content-center"><i class="bi bi-house"></i></div><div class="ps-3"><h6>'+form[1]["value"]+'</h6></div><div class="delete-regular-day-form"><form action="" name="delete-nh-record-form" class="delete-nh-record-form"><input type="hidden" name="csrfmiddlewaretoken" value="'+csrf+'"><input type="hidden" name="territory" value="'+territory_id+'"><input type="hidden" name="street" value="'+street_id+'"><input type="hidden" name="nh-record" value="'+house_id+'"><a class="btn btn-danger btn-sm edit-invite-button delete-nh-record-button"><i class="bi bi-trash"></i></a></form></div></div></div></div></div><!-- End Sales Card --></div>');
                    $('.modal').hide();
                    $('.modal-backdrop').remove();
                } else {
                    $('.houses').append('<div class="row house"><!-- Sales Card --><div class="col"><div class="card info-card invite-card"><div class="card-body invite-card-body"><div class="d-flex align-items-center"><div class="card-icon rounded-circle d-flex align-items-center justify-content-center"><i class="bi bi-house"></i></div><div class="ps-3"><h6>'+form[1]["value"]+'</h6></div><div class="delete-regular-day-form"><form action="" name="delete-nh-record-form" class="delete-nh-record-form"><input type="hidden" name="csrfmiddlewaretoken" value="'+csrf+'"><input type="hidden" name="territory" value="'+territory_id+'"><input type="hidden" name="street" value="'+street_id+'"><input type="hidden" name="nh-record" value=""><a class="btn btn-danger btn-sm edit-invite-button delete-nh-record-button"><i class="bi bi-trash"></i></a></form></div></div></div></div></div><!-- End Sales Card --></div>');
                    $('.modal').hide();
                    $('.modal-backdrop').remove();
                }
            }
        });
    }
});

$('.delete-nh-record-button').click(function() {
    var form = $(this).closest('.delete-nh-record-form').serializeArray();
    var csrf = form[0]["value"];
    var territory_id = form[1]["value"];
    var street_id = form[2]["value"];
    var house_id = form[3]["value"];
    $.ajax({
        type: "POST",
        url: "/service/my_territory/" + territory_id + "/nh_records/" + street_id + "/" + house_id + "/delete/",
        data: {
            "form": form,
        },
        headers: {
            'X-CSRFToken': csrf,
        },
        contentType: "application/javascript",
        dataType: "json",
        success: function(data) {
            $('.house-'+house_id).remove();
        }
    });
});