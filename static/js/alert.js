$(document).ready(function() {
    if ($(window).width() < 1200) {
        if($('body').hasClass('toggle-sidebar')) {
            $('.alert-svg').css({"margin-left":"305px"});
        } else {
            $('.alert-svg').css({"margin-left":"0px"});
        }
    
        $('.toggle-sidebar-btn').click(function(){
            if($('body').hasClass('toggle-sidebar')) {
                $('.alert-svg').css({"margin-left":"305px"});
            } else {
                $('.alert-svg').css({"margin-left":"0px"});
            }
        })
    } else {
        if($('body').hasClass('toggle-sidebar')) {
            $('.alert-svg').css({"margin-left":"0px"});
        } else {
            $('.alert-svg').css({"margin-left":"305px"});
        }
    
        $('.toggle-sidebar-btn').click(function(){
            if($('body').hasClass('toggle-sidebar')) {
                $('.alert-svg').css({"margin-left":"0px"});
            } else {
                $('.alert-svg').css({"margin-left":"305px"});
            }
        })
    }
});


$(window).on('resize', function(){
    if ($(window).width() < 1200) {
        if($('body').hasClass('toggle-sidebar')) {
            $('.alert-svg').css({"margin-left":"305px"});
        } else {
            $('.alert-svg').css({"margin-left":"0px"});
        }
    
        $('.toggle-sidebar-btn').click(function(){
            if($('body').hasClass('toggle-sidebar')) {
                $('.alert-svg').css({"margin-left":"305px"});
            } else {
                $('.alert-svg').css({"margin-left":"0px"});
            }
        })
    } else {
        if($('body').hasClass('toggle-sidebar')) {
            $('.alert-svg').css({"margin-left":"0px"});
        } else {
            $('.alert-svg').css({"margin-left":"305px"});
        }
    
        $('.toggle-sidebar-btn').click(function(){
            if($('body').hasClass('toggle-sidebar')) {
                $('.alert-svg').css({"margin-left":"0px"});
            } else {
                $('.alert-svg').css({"margin-left":"305px"});
            }
        })
    }
});