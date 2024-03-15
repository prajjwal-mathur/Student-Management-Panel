function get_all_class() {
  $.get("http://localhost:5000/class-subjects", function (data, status) {
    let details = data.data;
    let table_details = "";
    for (let i = 0; i < details.length; i++) {
      table_details =
        table_details +
        `<tr>
            <td>
          ${details[i]["id"]}
          </td>
          <td>
          ${details[i]["classNo"]}
          </td> 
          <td>
          ${details[i]["subjectNames"]}
          </td>
          <td> 
            <button class='btn btn-primary btn-sm edit-btn-${details[i]["id"]}' onclick="dialogBox('put','${details[i]["id"]}', '${details[i]["classNo"]}');" style='margin:5px'>Edit</button>
            <button class='btn btn-danger btn-sm del-btn-${details[i]["id"]}' onclick='delete_class("${details[i]["id"]}")'>Delete</button>
            </td>
          </tr>`;
    }

    document.getElementById("tableid").innerHTML = table_details;
  });
}


function makeDropdown() {
  $.get("http://localhost:5000/subjects", function (data, status) {
    var details = data.data;
    var droplist = `<option value="" disabled selected><i>Select a class</i></option>`;
    for (let i = 0; i < details.length; i++) {
      droplist =
        `${droplist}
        <option value='${details[i]["id"]}'>${details[i]["name"]}</option>
        `;
    }

    document.getElementById("subjects").innerHTML = droplist;
  });
}

// FOR DIALOG BOX
function dialogBox(method, classNo = "", className) {

  document.getElementById("responseMessage").textContent = "";
  const add_dialog = document.getElementById("addDialog");
  const closeBtn = document.getElementById("closeBtn");

  const form = document.getElementById("class-entry");
  form.setAttribute("data-method", method);
  form.setAttribute("data-classNo", classNo);


  if (method === "post") {

    document.getElementById("class-entry").reset();
    document.getElementById('entry-header').innerHTML = "Class entry form";
    document.getElementById("cname-label").innerHTML = "Enter a class"
    makeDropdown();
    if (!add_dialog.open) {
      add_dialog.showModal();
    }

    closeBtn.addEventListener("click", () => {
      add_dialog.close();
    });

  }
  else if (method === "put") {

    document.getElementById("class-entry").reset();
    document.getElementById('entry-header').innerHTML = "Class edit form";
    document.getElementById("cname-label").innerHTML = "Enter new unique class";
    document.getElementById('cname').value = className;
    makeDropdown();
    if (!add_dialog.open) {
      add_dialog.showModal();
    }

    closeBtn.addEventListener("click", () => {
      add_dialog.close();
    });

  }
}
const form = document.getElementById("class-entry");
form.addEventListener('submit', (event) => {
  event.preventDefault();
  let method = form.getAttribute("data-method");
  if (method === "post") {
    post_class();
  } else if (method === "put") {
    let classNo = form.getAttribute("data-classNo");

    put_class(classNo);
  } else if (method === "delete") {
    delete_class(classNo);
  }
})


//POST FORM DATA FROM SUBMIT BUTTON
function post_class() {
  const form = document.getElementById("class-entry");
  const responseMessage = document.getElementById("responseMessage")
  const select = document.getElementById("subjects")

  const selectedOptions = [];
  for (const option of select.options) {
    if (option.selected) {
      selectedOptions.push(parseInt(option.value));
    }
  }
  const classData = {
    'classNo': form.elements['cname'].value,
    subjectNo: selectedOptions
  }
  jsonData = JSON.stringify(classData)
  $.ajax({
    type: "POST",
    url: "http://localhost:5000/class-subjects",
    data: jsonData,
    contentType: "application/json",
    success: function (response) {
      responseMessage.textContent = `${classData['classNo']} has ${selectedOptions.length} subjects. ` + response?.message;
      get_all_class();
    },
    error: function (response) {
      console.log(response.responseJSON)
      responseMessage.textContent = response?.responseJSON?.classNo?.error;
    }
  })
}


function put_class(classNo) {

  const form = document.getElementById("class-entry");
  const responseMessage = document.getElementById("responseMessage")
  const select = document.getElementById("subjects")

  const selectedOptions = [];
  for (const option of select.options) {
    if (option.selected) {
      selectedOptions.push(parseInt(option.value));
    }
  }
  const classData = {
    'classNo': form.elements['cname'].value,
    subjectNo: selectedOptions
  }
  const jsonData = JSON.stringify(classData);

  $.ajax({
    type: "PUT",
    url: "http://localhost:5000/class-subjects/" + classNo,
    data: jsonData,
    contentType: "application/json",
    success: function (response) {
      responseMessage.textContent =
        "Class edited successfully: " + response?.message;
      get_all_class();
    },
    error: function (response) {
      console.log(response)
      responseMessage.textContent = response?.responseJSON?.classNo?.[0];
    },
  });
  setTimeout(function () {
    document.getElementById("cname").value = "";
  }, 1000);
}

function delete_class(classNo) {
  $.ajax({
    type: "DELETE",
    url: "http://localhost:5000/class-subjects/" + classNo,
    success: function (response) {
      get_all_class();
    },
  })
}