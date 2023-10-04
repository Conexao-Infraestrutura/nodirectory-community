var table_users = window.document.getElementById("table_users");

function populate_users() 
{
    $.ajax({
        url: '/userlist',
        type: 'POST',
        async: 'false',
        success: function(userlist_return)
        {
            
            for (i=0; i < userlist_return.uids.length; i++)
            {
                let row = table_users.insertRow([i]);

                let cell0 = row.insertCell(0);
                let cell1 = row.insertCell(1);
                let cell2 = row.insertCell(2);
                
                cell0.innerText = userlist_return.uids[i];
                
                cell1.innerText = userlist_return.usernames[i];

                let btninfo = document.createElement("input");
                btninfo.type = "button";
                btninfo.value = "info";
                btninfo.className = "btn btn-primary btn-sm";
                btninfo.setAttribute("onclick", `getUserInfo(${userlist_return.uids[i].trim()})`);

                let btndelete = document.createElement("input");
                btndelete.type = "button";
                btndelete.value = "delete";
                btndelete.className = "btn btn-danger btn-sm";
                btndelete.setAttribute("onclick", `deleteUserInfo(${userlist_return.uids[i].trim()})`);
                btndelete.setAttribute("data-bs-toggle", "modal");
                btndelete.setAttribute("data-bs-target", "#modal_confirm");

                let btnpass = document.createElement("input");
                btnpass.type = "button";
                btnpass.value = "password";
                btnpass.className = "btn btn-secondary btn-sm";
                btnpass.setAttribute("onclick", `passwordUserInfo(${userlist_return.uids[i].trim()})`);
                btnpass.setAttribute("data-bs-toggle", "modal");
                btnpass.setAttribute("data-bs-target", "#modal_formpass");

                cell2.className = "d-flex gap-1";
                cell2.appendChild(btninfo);
                cell2.appendChild(btndelete);
                cell2.appendChild(btnpass);
            }
        }
    });
}

function swapUidNumber(inputvar) {
    delete uid_number;
    uid_number = inputvar;
}

function swapInfoState(inputvar) {
    delete info_state;
    info_state = inputvar;
}

swapInfoState('off');
swapUidNumber(0);

function getUserInfo(user_info_get)
{
    console.log('infoshowed: ' + info_state + ', uid: ' + uid_number);

    function uidInfoShow(user_info_get)
    {
        var table_info = window.document.getElementById("table_userinfo");
        let postdata = `&uid=${user_info_get}`;
        $.ajax({
            url: '/userinfo',
            type: 'POST',
            data: postdata,
            datatype: 'json',
            async: 'false',
            success: function(userinfo_return)
            {
                table_info.innerHTML = "";
                let row = table_info.insertRow(0);
                let cell0 = row.insertCell(0);

                for (i=0; i< userinfo_return.info.length; i++)
                {
                    cell0.innerHTML = cell0.innerHTML + userinfo_return.info[i] + "<br>";
                }
            }
        });
    }

    if(user_info_get != uid_number && info_state != 'on')
    {
        uidInfoShow(user_info_get);
        swapUidNumber(user_info_get);
        swapInfoState('on');
    }
    else if(user_info_get == uid_number && info_state != 'on')
    {
        uidInfoShow(user_info_get);
        swapUidNumber(user_info_get);
        swapInfoState('on');
    }
    else if(user_info_get != uid_number && info_state == 'on')
    {
        uidInfoShow(user_info_get);
        swapUidNumber(user_info_get);
        swapInfoState('on');
    }
    else
    {
        $( "#table_userinfo" ).empty();
        swapInfoState('off');
    }
}

function deleteUserInfo(user_info_get){

    $( "#modal_confirm_title" ).text( "Delete User" );
    $( "#modal_confirm_text" ).text( "Are you sure you want to delete it !?" )
    $( "#modal_confirm_btnok" ).click(function(){

        let postdata = `&uid=${user_info_get}`;

        $.ajax({
            url: '/userdel',
            type: 'POST',
            data: postdata,
            datatype: 'json',
            async: 'false',
            success: function(userdel_return)
            {
                if (userdel_return.result == 'ok')
                {
                    $( "#modal_notify_title" ).text( "Delete User" );
                    $( "#modal_notify_text" ).text( "The user was deleted" );
                }
                else
                {
                    $( "#modal_notify_title" ).text( "Delete User" );
                    $( "#modal_notify_text" ).text( "Problem: " + userdel_return.message );
                    $( "#modal_notify_text" ).addClass("text-danger");
                }
            }
        });
    })
}

function addUserInfo()
{   

    $( "#modal_form_add_title" ).text( "Add User" );
    $( "#form_add_input_user_name" ).val("");
    $( "#form_add_select_usergroup_name" ).find('option').remove();
    $( "#form_add_select_usersupgroups_name" ).find('option').remove();    
    let user_samba = 'checked';

    const smb_user_check = window.document.getElementById("form_add_check_user_smb");
    const user_name_input = window.document.getElementById("form_add_input_user_name");
    const user_name_submit = window.document.getElementById("modal_form_add_btnok");
    const user_prim_group = window.document.getElementById("form_add_select_usergroup_name");
    const user_comp_group = window.document.getElementById("form_add_select_usersupgroups_name");
 
    function define_smb_checkstate()
    {
        if (smb_user_check.checked == false) 
        { 
            user_samba = 'unchecked';
        }
    }

    function primgroup_get()
    {
        $.ajax({
            url: '/grouplist',
            type: 'POST',
            async: 'false',
            success: function(groupname_return)
            {
                for(i=0; i < groupname_return.groupnames.length; i++)
                {
                    user_prim_group.add(new Option(groupname_return.groupnames[i].trim(), groupname_return.gids[i].trim()));
                }
            }
        });
    }

    function compgroup_get()
    {
        $.ajax({
            url: '/grouplist',
            type: 'POST',
            async: 'false',
            success: function(groupname_return)
            {
                for(i=0; i < groupname_return.groupnames.length; i++)
                {
                    user_comp_group.add(new Option(groupname_return.groupnames[i].trim(), groupname_return.gids[i].trim()));
                }
            }
        });
    }

    function submit_input_username() {
        if (!Boolean(user_name_input.value.match(/^[A-Za-z0-9]*$/)))
        {
            $( "#modal_notify_title" ).text( "Add User" );
            $( "#modal_notify_text" ).text( "Problem: Especial characters aren't permitted in the user name" );
            $( "#modal_notify_text" ).addClass("text-danger");
        }
        else if (user_name_input.value == '') 
        {
            $( "#modal_notify_title" ).text( "Add User" );
            $( "#modal_notify_text" ).text( "Problem: User name can't be blank" );
            $( "#modal_notify_text" ).addClass("text-danger");
        }
        else
        {

            let ret_comp_groups = [];

            function incrementCompGroups(input_group){
                ret_comp_groups.push(input_group);
            }

            for (i=0; i < user_comp_group.options.length; i++){
                if (user_comp_group.options[i].selected == true){
                    incrementCompGroups(user_comp_group.options[i].value);
                }
            }

            let postdata = `&username=${user_name_input.value}
                            &smbuser=${user_samba}
                            &primgroup=${user_prim_group.value}
                            &supgroups=${ret_comp_groups}`;
            $.ajax({
                url: '/useradd',
                type: 'POST',
                data: postdata,
                datatype: 'json',
                async: 'false',
                success: function(useradd_return)
                {
                    if (useradd_return.result == 'ok')
                    {
                        $( "#modal_notify_title" ).text( "Add User" );
                        $( "#modal_notify_text" ).text( "The user was added");
                    }
                    else
                    {
                        $( "#modal_notify_title" ).text( "Add User" );
                        $( "#modal_notify_text" ).text( "Problem: " + useradd_return.message );
                        $( "#modal_notify_text" ).addClass("text-danger");
                    }
                }
            });
        }
    }

    smb_user_check.addEventListener("change", define_smb_checkstate);
    user_name_submit.addEventListener("click", submit_input_username);
    primgroup_get();
    compgroup_get();
}

function passwordUserInfo(uid) {

    $( "#modal_formpass_title" ).text("Change Password");
    $( "#formpass_input_first" ).val("");
    $( "#formpass_input_second" ).val("");

    const formpass_first = window.document.getElementById("formpass_input_first");
    const formpass_second = window.document.getElementById("formpass_input_second");


    $("#modal_formpass_btnok").click(function () { 

    let first_pass = formpass_first.value;
    let second_pass = formpass_second.value;

        if (first_pass == "")
        {
            $( "#modal_notify_title" ).text( "Add User" );
            $( "#modal_notify_text" ).text( "Fill the two password fields" );
            $( "#modal_notify_text" ).addClass("text-danger");
        }
        else if (second_pass == "")
        {
            $( "#modal_notify_title" ).text( "Add User" );
            $( "#modal_notify_text" ).text( "Fill the two password fields" );
            $( "#modal_notify_text" ).addClass("text-danger");
        }
        else if (first_pass != second_pass)
        {
                $( "#modal_notify_title" ).text( "Add User" );
                $( "#modal_notify_text" ).text( "Passwords are diferent" );
                $( "#modal_notify_text" ).addClass("text-danger");
        }
        else
        {

            let postdata = `&uid=${uid}&pass=${first_pass}`;

            $.ajax({
                url: '/userpass',
                type: 'POST',
                data: postdata,
                datatype: 'json',
                success: function(userpass_return)
                {
                    {
                        if (userpass_return.result == 'ok')
                        {
                            $( "#modal_notify_title" ).text( "User Password" );
                            $( "#modal_notify_text" ).text( "The user password was changed");
                        }
                        else
                        {
                            $( "#modal_notify_title" ).text( "User Password" );
                            $( "#modal_notify_text" ).text( "Problem: " + useradd_return.message );
                            $( "#modal_notify_text" ).addClass("text-danger");
                        }
                    }
                }
            });
        }
    });
}

window.addEventListener("load", populate_users);