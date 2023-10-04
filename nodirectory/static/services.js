let table_services = window.document.getElementById("table_services");

function populate_services() 
{
    $.ajax({
        url: '/servicelist',
        type: 'POST',
        async: 'false',
        success: function(servicelist_return)
        {
            for (i=0; i < servicelist_return.services.length; i++)
            {
                let row = table_services.insertRow([i]);

                let cell0 = row.insertCell(0);
                let cell1 = row.insertCell(1);
                
                cell0.innerText = servicelist_return.services[i][0];
                cell1.innerText = servicelist_return.services[i][1];
            }
        }
    });
}

window.addEventListener("load", populate_services);
