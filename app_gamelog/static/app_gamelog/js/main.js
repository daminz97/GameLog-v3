// csrf_token setup
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i=0; i<cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length+1) === (name+'=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length+1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

if (!csrftoken || csrftoken == "") {
    alert("Cookie disabled");
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// user profile edit form toggle
$("#profile-edit-btn").click(function(e){
    e.preventDefault();
    if ($(".update-avatar-container").css('display') == 'block') {
        $(".update-avatar-container").css('display', 'none');
    }
    $(".update-form-container").fadeToggle(300);
});
// user profile update
$("#update-profile-submit").click(function(e) {
    e.preventDefault();
    if ($("#id_email").val() == '' && $("#id_fname").val() == '' && $("#id_lname").val() == '') {
        alert('Please complete all fields.');
    } else {
        $.ajax({
            type: "POST",
            url: "new_profile",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                new_email: $("#id_email").val(),
                new_fname: $("#id_fname").val(),
                new_lname: $("#id_lname").val()
            },
            success: function(data) {
                $("#user-fullname").html(data.fullname);
                $("#user-email").html(data.email);
                $("#user-fname").html(data.fname);
                $("#user-lname").html(data.lname);
            },
        });
        $("#update-profile-form")[0].reset();
        $(".update-form-container").fadeOut(300);
    }
});
// user change password
$("#reset-pass-submit").click(function(e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: 'change_pass',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            old_password: $("#id_old_password").val(),
            new_password: $("#id_new_password").val(),
            verify_password: $("#id_verify_password").val()
        },
        success: function(data) {
            $("#authentication-status").html(data.msg);
            $(".authentication-bar-status").append('<meta http-equiv="refresh" content="3;url=\'logout\'"></meta>');
        }
    })
})
// check if old password
$("#id_old_password").keyup(function() {
    $.ajax({
        type: "GET",
        url: "check_old_password",
        headers: {'X-CSRFToken': csrftoken},
        data: {
            keyin_password: $("#id_old_password").val().trim()
        },
        success: function(data) {
            $("#authentication-status").text(data.msg)
        },
    });
});
// check if new same as old
$("#id_new_password").keyup(function() {
    $.ajax({
        type: "GET",
        url: "check_match_old_password",
        headers: {'X-CSRFToken': csrftoken},
        data: {
            old_password: $("#id_old_password").val().trim(),
            new_password: $("#id_new_password").val().trim(),
        },
        success: function(data) {
            $("#authentication-status").text(data.msg)
        }
    })
})
// check if passwords match
$("#id_verify_password").keyup(function() {
    $.ajax({
        type: "GET",
        url: "check_match_password",
        headers: {'X-CSRFToken': csrftoken},
        data: {
            new_password: $("#id_new_password").val().trim(),
            verify_password: $("#id_verify_password").val().trim(),
        },
        success: function(data) {
            $("#authentication-status").text(data.msg)
        },
    });
});

// user avatar edit form toggle
$("#avatar-btn").click(function(e){
    e.preventDefault();
    if ($(".update-form-container").css('display') == 'block') {
        $(".update-form-container").css('display', 'none');
    }
    $(".update-avatar-container").fadeToggle(300);
});
$("#update-avatar-close").click(function(e){
    e.preventDefault();
    $(".update-avatar-container").fadeOut(300);
});
// user avatar update
$("#update-avatar-submit").click(function(e){
    e.preventDefault();
    if ($('input[name=avatars]:checked', '#update-avatar-form').length == 0) {
        alert('Please select your desired avatar.');
    } else {
        $.ajax({
            type: "POST",
            url: "new_avatar",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                new_avatar: $('input[name=avatars]:checked', '#update-avatar-form').val()
            },
            success: function(data) {
                $("#avatar").attr('src', data.avatar);
                $(".update-avatar-container").fadeOut(300);
            },
        });
    }
});

// games show search bar btn
$("#show-nav-btn").click(function(e){
    e.preventDefault();
    $("#pills-tabContent").fadeToggle(300);
    $("i", this).toggleClass('fa-arrow-circle-left fa-arrow-circle-down');
});

// search by other
$("#search-other-submit").click(function(e){
    e.preventDefault();
    if ($("#id_search_platform").val() == '' && $("#id_search_genre").val() == '') {
        alert('Please select a platform or a genre.');
    } else {
        $("#search-other-status").html('');
        $.ajax({
            type: "GET",
            url: 'games/search_by_other',
            headers: {'X-CSRFToken': csrftoken},
            data: {
                search_platform: $("#id_search_platform").val(),
                search_genre: $("#id_search_genre").val()
            },
            success: function(data) {
                $("#games-content").html(data);
                $("#search-other-status").html(data.error);
            },
        });
        $("#search-other-form")[0].reset();
    }
});
// search by name
$("#search-name-submit").click(function(e){
    e.preventDefault();
    if ($("#id_search_name").val() == '') {
        alert('Please enter a game name.');
    } else {
        $("#search-name-status").html('');
        $.ajax({
            type: "GET",
            url: "games/search_by_name",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                search_name: $("#id_search_name").val()
            },
            success: function(data) {
                $("#games-content").html(data);
                $("#search-name-status").html(data.error);
            },
        });
        $("#search-name-form")[0].reset();
    }
});

// add game
$("#add-submit").click(function(e) {
    e.preventDefault();
    if ($("#id_add_name").val() == '' || $("#id_add_platform").val() == '' || $("#id_add_genre").val() == '' || $("#id_add_image_url").val() == '') {
        alert('Please complete all fields.');
    } else {
        $.ajax({
            type: "POST",
            url: "games/add_game",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                add_name: $("#id_add_name").val(),
                add_platform: $("#id_add_platform").val(),
                add_genre: $("#id_add_genre").val(),
                add_image_url: $("#id_add_image_url").val()
            },
            success: function(data) {
                $("#add-game-status").html(data.msg);
            },
        });
        $("#add-game-form")[0].reset();
    }
});

// add game to library toggle
$(".add-game-toggle-btn").click(function(e) {
    e.preventDefault();
    $(".add-to-library-form-container").fadeToggle(300);
})
// add log toggle
$("#add-game-log-submit").click(function(e) {
    e.preventDefault();
    $(".add-log-form-container").fadeToggle(300);
})

// publish game toggle
$("#publish-game-btn").click(function(e) {
    e.preventDefault();
    $(".publish-game-container").fadeToggle(300);
})

// // feeds
// $(".card-close-btn").click(function(e){
//     e.preventDefault();
//     (".card").css('display', 'none');
// });