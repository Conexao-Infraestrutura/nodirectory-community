const login_button = window.document.getElementById('form_auth_btn_login')
const user_auth = window.document.getElementById('form_auth_input_user_name')
const user_pass = window.document.getElementById('form_auth_input_user_pass')
const login_error = window.document.getElementById('alert_login_error')

$(user_auth).val('');
$(user_pass).val('');

$(login_button).click(function () {
    let user = $(user_auth).val();
    let pass = $(user_pass).val();
    let postdata = `sent_user=${user}&sent_pass=${pass}`
    $.ajax({
        type: "POST",
        url: "/logsession",
        data: postdata,
        dataType: "json",
        success: function (login_return) {
            if (login_return.result == 'ok'){
                window.location = 'service';
            }
            else
            {
                $(login_error).removeClass('d-none');
            }
        }
    });
});
