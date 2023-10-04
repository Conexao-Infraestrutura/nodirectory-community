const btn_user_menu = window.document.getElementById('user_menu');

function sess_user () {
    $.ajax({
        type: "POST",
        url: "/loggeduser",
        success: function (front_return) {
            $(btn_user_menu).text(front_return.result);
        }
    });
}

window.addEventListener('load', sess_user);
