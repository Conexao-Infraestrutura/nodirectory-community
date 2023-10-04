// Create visualization os present machines
var table_machines = window.document.getElementById("table_machines");
function populateMachines() 
{
    $.ajax({
        url: '/machinelist',
        type: 'POST',
        async: 'false',
        success: function(machinelist_return)
        {
            
            for (i=0; i < machinelist_return.uids.length; i++)
            {
                let row = table_machines.insertRow([i]);

                let cell0 = row.insertCell(0);
                let cell1 = row.insertCell(1);
                let cell2 = row.insertCell(2);
                
                cell0.innerText = machinelist_return.uids[i];
                
                cell1.innerText = machinelist_return.machinenames[i];

                let btndelete = document.createElement("input");
                btndelete.type = "button";
                btndelete.value = "delete";
                btndelete.className = "btn btn-danger btn-sm";
                btndelete.setAttribute("onclick", `deleteMachineInfo(${machinelist_return.uids[i].trim()})`);
                btndelete.setAttribute("data-bs-toggle", "modal");
                btndelete.setAttribute("data-bs-target", "#modal_confirm");

                cell2.className = "d-flex gap-1";
                cell2.appendChild(btndelete);
            }
        }
    });
}

// Remove a machine
function deleteMachineInfo(machine_info_get){

    $( "#modal_confirm_title" ).text( "Delete Machine" );
    $( "#modal_confirm_text" ).text( "Are you sure you want to delete it !?" )
    $( "#modal_confirm_btnok" ).click(function(){

        let postdata = `&uid=${machine_info_get}`;

        $.ajax({
            url: '/machinedel',
            type: 'POST',
            data: postdata,
            datatype: 'json',
            async: 'false',
            success: function(machinedel_return)
            {
                if (machinedel_return.result == 'ok')
                {
                    $( "#modal_notify_title" ).text( "Delete Machine" );
                    $( "#modal_notify_text" ).text( "The machine was deleted" );
                }
                else
                {
                    $( "#modal_notify_title" ).text( "Delete Machine" );
                    $( "#modal_notify_text" ).text( "Problem: " + machinedel_return.message );
                    $( "#modal_notify_text" ).addClass("text-danger");
                }
            }
        });
    })
}

function addMachineInfo()
{   

    $( "#modal_form_add_machine_title" ).text( "Add Machine" );
    $( "#form_add_input_machine_credentials" ).val("");
    $( "#form_add_input_password_credentials" ).val("");
    $( "#form_add_input_sudo_password_credentials" ).val("");
    $( "#form_add_input_sudo_password_credentials" ).prop('disabled', true);
    $( "#form_add_select_pass_or_key" ).prop('checked', false)

    const machine_credentials = window.document.getElementById("form_add_input_machine_credentials");
    const password_credentials = window.document.getElementById("form_add_input_password_credentials");
    const password_sudo_credentials = window.document.getElementById("form_add_input_sudo_password_credentials");
    const machine_pass_or_key = window.document.getElementById("form_add_select_pass_or_key");
    const add_machine_btnok = window.document.getElementById("modal_form_add_machine_btnok");
    
    let pass_or_key = 'unchecked';
    function definePassOrKeycheckstate()
    {
        if (machine_pass_or_key.checked == true) 
        { 
            pass_or_key = 'checked';
            $( "#form_add_input_sudo_password_credentials" ).prop('disabled', false);
        }
        else
        {
            pass_or_key = 'unchecked';
            $( "#form_add_input_sudo_password_credentials" ).prop('disabled', true);
        }
    }

    function executeMachineIngress() {

        let postdata = `&cred=${encodeURIComponent(machine_credentials.value)}
                        &auth=${encodeURIComponent(password_credentials.value)}
                        &sudo=${encodeURIComponent(password_sudo_credentials.value)}
                        &passkey=${pass_or_key}`;
       
        $.ajax({
            url: '/machineadd',
            type: 'POST',
            data: postdata,
            datatype: 'json',
            async: 'false',
            success: function(machineadd_return)
            {
                if (machineadd_return.result == 'ok')
                {
                    $( "#modal_notify_title" ).text( "Add Machine" );
                    $( "#modal_notify_text" ).text( "The machine was sucessfull Ingressed");
                }
                else
                {
                    $( "#modal_notify_title" ).text( "Add Machine" );
                    $( "#modal_notify_text" ).text( "Problem: " + machineadd_return.message);
                    $( "#modal_notify_text" ).addClass("text-danger");
                }
            }
        });
    }

    machine_pass_or_key.addEventListener("change", definePassOrKeycheckstate);
    add_machine_btnok.addEventListener("click", executeMachineIngress);

}

window.addEventListener("load", populateMachines);