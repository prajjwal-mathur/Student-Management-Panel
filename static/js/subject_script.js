function get_all_subjects() {
    $.get("http://localhost:5000/subjects", function (data, status) {
        var details = data.data;
        console.log(details)
        var table_details = "";
        for (let i = 0; i < details.length; i++) {
            table_details =
                table_details +
                `<tr>
                    <td style="padding-left: 50px; padding-right: 50px">
                        ${details[i]["id"]}
                    </td>
                    <td style="padding:50px">
                        ${details[i]["name"]}
                    </td>
                    <td style="padding:50px">
                        ${details[i]["passing"]}
                    </td>
                    <td style="padding:50px">
                        ${details[i]["total"]}
                    </td>
                    <td style="padding:50px"> 
                        <button class='btn btn-primary btn-sm edit-btn-${details[i]["id"]}' onclick="dialogBox('put','${details[i]["id"]}')" style='margin:2px'>Edit</button>
                        <button class='btn btn-danger btn-sm del-btn-${details[i]["id"]}' onclick='delete_subject("${details[i]["id"]}")'>Delete</button>
                    </td>
                </tr>`;
        }


        document.getElementById("tableid").innerHTML = table_details;
    });
}

function dialogBox(method, subId = "") {
    
    document.getElementById("responseMessage").textContent = "";
    const add_dialog = document.getElementById("addDialog");
    const closeBtn = document.getElementById("closeBtn");

    const form = document.getElementById("sub-entry");
    form.setAttribute("data-method", method);
    form.setAttribute("data-subId", subId);

    if (method === "post") {

        document.getElementById("sub-entry").reset();
        document.getElementById('entry-header').innerHTML = "Subject entry form";
        document.getElementById("sname-label").innerHTML = "Enter subject name";
        document.getElementById("pmarks-label").innerHTML = "Enter passing marks";
        document.getElementById("tmarks-label").innerHTML = "Enter total marks";

        if (!add_dialog.open) {
            add_dialog.showModal();
        }

        closeBtn.addEventListener("click", () => {
            add_dialog.close();
        });

    }
    else if (method === "put") {

        document.getElementById("sub-entry").reset();
        document.getElementById('entry-header').innerHTML = "Subject edit form";
        document.getElementById("sname-label").innerHTML = "Enter unique subject name";
        document.getElementById("pmarks-label").innerHTML = "Enter passing marks";
        document.getElementById("tmarks-label").innerHTML = "Enter total marks";

       
        if (!add_dialog.open) {
            add_dialog.showModal();
        }

        closeBtn.addEventListener("click", () => {
            add_dialog.close();
        });

    }
}


function submit_form() {
    const form = document.getElementById("sub-entry");
    let method = form.getAttribute("data-method");
    
    if (method === "post") {
        post_subject();
    } else if (method === "put") {
        put_subject();
    }
}

function post_subject() {
    let form = document.getElementById("sub-entry");
    let responseMessage = document.getElementById("responseMessage");
    event.preventDefault();

    const subData = {
        name: form.elements['sname'].value,
        passing: parseFloat(form.elements['pmarks'].value),
        total: parseFloat(form.elements['tmarks'].value)
    };
   

    const jsonData = JSON.stringify(subData);
   
    $.ajax({
        type: "POST",
        url: "http://localhost:5000/subjects",
        data: jsonData,
        contentType: "application/json",
        success: function (response) {
            responseMessage.textContent = "Subject added successfully: " + response?.message;
            get_all_subjects();
        },
        error: function (response) {

            errorMessage = ""
            if (response?.responseJSON?.name?.[0] != undefined) {
                errorMessage += response?.responseJSON?.name?.[0]
            }; if (response?.responseJSON?.passing?.[0] != undefined) {
                errorMessage += " " + response?.responseJSON?.passing?.[0];
            }; if (response?.responseJSON?.total?.[0] != undefined) {
                errorMessage += " " + response?.responseJSON?.total?.[0];
            };
            responseMessage.textContent = errorMessage
        },
    });
    setTimeout(function () {
        document.getElementById("sname").value = "";
        document.getElementById("pmarks").value = "";
        document.getElementById("tmarks").value = "";
    }, 1500);
}

function put_subject() {
    
    let form = document.getElementById("sub-entry");
    let responseMessage = document.getElementById("responseMessage");

    event.preventDefault();

    const subData = {
        name: form.elements['sname'].value,
        passing: parseFloat(form.elements['pmarks'].value),
        total: parseFloat(form.elements['tmarks'].value)
    };

    const jsonData = JSON.stringify(subData);

    $.ajax({
        type: "PUT",
        url: "http://localhost:5000/subjects/" + form.getAttribute("data-subId"),
        data: jsonData,
        contentType: "application/json",
        success: function (response) {
            responseMessage.textContent = "Subject edited successfully: " + response?.message;
            get_all_subjects();
        },
        error: function (response) {

            errorMessage = ""
            if (response?.responseJSON?.name?.[0] != undefined) {
                errorMessage += response?.responseJSON?.name?.[0]
            }; if (response?.responseJSON?.passing?.[0] != undefined) {
                errorMessage += " " + response?.responseJSON?.passing?.[0];
            }; if (response?.responseJSON?.total?.[0] != undefined) {
                errorMessage += " " + response?.responseJSON?.total?.[0];
            };
            responseMessage.textContent = errorMessage
        },
    });
    setTimeout(function () {
        document.getElementById("sname").value = "";
        document.getElementById("pmarks").value = "";
        document.getElementById("tmarks").value = "";
    }, 1500);
}


function delete_subject(subId) {
    $.ajax({
        type: "DELETE",
        url: "http://localhost:5000/subjects/" + subId,
        success: function (response) {
            responseMessage.textContent =
                "Subject deleted successfully: " + response?.message;
            get_all_subjects();
        },
        error: function (response) {
            responseMessage.textContent = response?.responseJSON?.id?.[0];
        },
    })
}