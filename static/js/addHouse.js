$('#add-house-button').click(function() {
    form = $('form').serializeArray();
    csrf = form[0]["value"];
    territory_id = form[2]["value"];
    street_id = form[3]["value"];
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
                $('.houses').append('<div class="row"><!-- Sales Card --><div class="col"><div class="card info-card invite-card"><div class="card-body invite-card-body"><div class="d-flex align-items-center"><divclass="card-icon rounded-circle d-flex align-items-center justify-content-center"><i class="bi bi-house"></i></divclass=><div class="ps-3"><h6>'+form[1]["value"]+'</h6></div><div class="delete-regular-day-form"><a class="btn btn-danger btn-sm edit-invite-button" href="#"><i class="bi bi-trash"></i></a></div></div></div></div></div><!-- End Sales Card --></div>');
                $('.modal').hide();
                $('.modal-backdrop').remove();
            }
        });
    }
});