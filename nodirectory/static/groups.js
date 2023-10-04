var table_groups = window.document.getElementById("table_groups");

function populate_groups() 
{
    $.ajax({
        url: '/grouplist',
        type: 'POST',
        async: 'false',
        success: function(grouplist_return)
        {
            
            for (i=0; i < grouplist_return.gids.length; i++)
            {
                let row = table_groups.insertRow([i]);

                let cell0 = row.insertCell(0);
                let cell1 = row.insertCell(1);
                let cell2 = row.insertCell(2);
                
                cell0.innerText = grouplist_return.gids[i];
                
                cell1.innerText = grouplist_return.groupnames[i];

                let btninfo = document.createElement("input");
                btninfo.type = "submit";
                btninfo.value = "info";
                btninfo.className = "btn btn-primary btn-sm";
                btninfo.setAttribute("onclick", `getGroupInfo(${grouplist_return.gids[i].trim()})`);

                let btndelete = document.createElement("input");
                btndelete.type = "submit";
                btndelete.value = "delete";
                btndelete.className = "btn btn-danger btn-sm";
                btndelete.setAttribute("onclick", `deleteGroupInfo(${grouplist_return.gids[i].trim()})`);
                btndelete.setAttribute("data-bs-toggle", "modal");
                btndelete.setAttribute("data-bs-target", "#modal_confirm");

                cell2.className = "d-flex gap-1";
                cell2.appendChild(btninfo);
                cell2.appendChild(btndelete);
            }
        }
    });
}

function swapGidNumber(inputvar) {
    delete gid_number;
    gid_number = inputvar;
}

function swapInfoState(inputvar) {
    delete info_state;
    info_state = inputvar;
}

swapInfoState('off');
swapGidNumber(0);

function getGroupInfo(group_info_get)
{
    console.log('infoshowed: ' + info_state + ', gid: ' + gid_number);

    function gidInfoShow(group_info_get)
    {
        var table_info = window.document.getElementById("table_groupinfo");
        let postdata = `&gid=${group_info_get}`;
        $.ajax({
            url: '/groupinfo',
            type: 'POST',
            data: postdata,
            datatype: 'json',
            async: 'false',
            success: function(groupinfo_return)
            {
                table_info.innerHTML = "";
                let row = table_info.insertRow(0);
                let cell0 = row.insertCell(0);

                for (i=0; i< groupinfo_return.info.length; i++)
                {
                    cell0.innerHTML = cell0.innerHTML + groupinfo_return.info[i] + "<br>";
                }
            }
        });
    }

    if(group_info_get != gid_number && info_state != 'on')
    {
        gidInfoShow(group_info_get);
        swapGidNumber(group_info_get);
        swapInfoState('on');
    }
    else if(group_info_get == gid_number && info_state != 'on')
    {
        gidInfoShow(group_info_get);
        swapGidNumber(group_info_get);
        swapInfoState('on');
    }
    else if(group_info_get != gid_number && info_state == 'on')
    {
        gidInfoShow(group_info_get);
        swapGidNumber(group_info_get);
        swapInfoState('on');
    }
    else
    {
        $( "#table_groupinfo" ).empty();
        swapInfoState('off');
    }
}

function deleteGroupInfo(group_info_get){

    $( "#modal_confirm_title" ).text( "Delete Group" );
    $( "#modal_confirm_text" ).text( "Are you sure you want to delete it !?" )
    $( "#modal_confirm_btnok" ).click(function(){

        let postdata = `&gid=${group_info_get}`;

        $.ajax({
            url: '/groupdel',
            type: 'POST',
            data: postdata,
            datatype: 'json',
            async: 'false',
            success: function(groupdel_return)
            {
                if (groupdel_return.result == 'ok')
                {
                    $( "#modal_notify_title" ).text( "Delete Group" );
                    $( "#modal_notify_text" ).text( "The group was deleted" );
                }
                else
                {
                    $( "#modal_notify_title" ).text( "Delete Group" );
                    $( "#modal_notify_text" ).text( "Problem: " + groupdel_return.message );
                    $( "#modal_notify_text" ).addClass("text-danger");
                }
            }
        });
    })
}

$( "#form_add_input_group_name" ).val("");
function addGroupInfo()
{   

    $( "#modal_form_add_title" ).text( "Add Group" );
    let group_samba = 'checked';

    const smb_group_check = window.document.getElementById("form_add_check_group_smb");
    const group_name_input = window.document.getElementById("form_add_input_group_name");
    const group_name_submit = window.document.getElementById("modal_form_add_btnok");
 
    function define_smb_checkstate() {
        if (smb_group_check.checked == false) 
        { 
            group_samba = 'unchecked';
        }
    }

    function submit_input_groupname() {
        if (!Boolean(group_name_input.value.match(/^[A-Za-z0-9]*$/)))
        {
            $( "#modal_notify_title" ).text( "Add Group" );
            $( "#modal_notify_text" ).text( "Problem: Especial characters aren't permitted in the group name" );
            $( "#modal_notify_text" ).addClass("text-danger");
        }
        else if (group_name_input.value == '') 
        {
            $( "#modal_notify_title" ).text( "Add Group" );
            $( "#modal_notify_text" ).text( "Problem: Group name can't be blank" );
            $( "#modal_notify_text" ).addClass("text-danger");
        }
        else
        {
            let postdata = `&groupname=${group_name_input.value}
                            &smbgroup=${group_samba}`;
            $.ajax({
                url: '/groupadd',
                type: 'POST',
                data: postdata,
                datatype: 'json',
                async: 'false',
                success: function(groupadd_return)
                {
                    if (groupadd_return.result == 'ok')
                    {
                        $( "#modal_notify_title" ).text( "Add Group" );
                        $( "#modal_notify_text" ).text( "The group was added");
                    }
                    else
                    {
                        $( "#modal_notify_title" ).text( "Add Group" );
                        $( "#modal_notify_text" ).text( "Problem: " + groupadd_return.message );
                        $( "#modal_notify_text" ).addClass("text-danger");
                    }
                }
            });
        }
    }

    smb_group_check.addEventListener("change", define_smb_checkstate);
    group_name_submit.addEventListener("click", submit_input_groupname);
}

window.addEventListener("load", populate_groups);
