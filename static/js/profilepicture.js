$('#id_profile_picture').change(function() {
    file = $(this)[0].files[0]
    if(file) {
        let reader = new FileReader();
        reader.onload = function (event) {
            $("#profile-picture-edit")
                .attr("src", event.target.result);
        };
        reader.readAsDataURL(file);
    }
});

$('#profile_picture-clear_id').click(function() {
    $('#profile-picture-edit').attr('src', '/media/noimage.webp');
});