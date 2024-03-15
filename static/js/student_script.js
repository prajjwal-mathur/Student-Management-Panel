function get_all_students() {
  $.get("http://localhost:5000/students", function (data, status) {
    var details = data.data;
    var table_details = "";

    for (let i = 0; i < details.length; i++) {
      table_details =
        `${table_details}
        <tr>
          <td>
            ${details[i]["id"]} 
          </td>
          <td>
            ${details[i]["name"]}
          </td>
          <td>
            ${details[i]["admissionYear"]}
          </td>
          <td>
            ${details[i]["classNo"]}
          </td>
          <td>
          ${details[i]["totalMarks"]}
          </td>
          <td> 
          <button class='btn btn-primary btn-sm edit-btn-${details[i]["id"]}' onclick="dialogBox('get', '${details[i]["id"]}')" style='margin:5px'>View Marksheet</button>
          <button class='btn btn-danger btn-sm del-btn-${details[i]["id"]}' onclick=delete_student("${(details[i]["id"])}") style='margin:5px'>Remove student</button>
          </td>
        </tr>`;
    }


    document.getElementById("tableid").innerHTML = table_details;
  });
}

{/* <td> 
            <button class='btn btn-primary btn-sm edit-btn-${details[i]["id"]}' onclick="dialogBox('put','${details[i]["id"]}')" style='margin:5px'>Edit</button>
            <button class='btn btn-danger btn-sm del-btn-${details[i]["id"]}' onclick='delete_student("${details[i]["id"]}")'>Delete</button>
          </td> */}

var subjectIds = [];
function get_student(roll_number) {
  const dialogBox = document.getElementById("marksheet");
  subjectIds = [];
  $.get(`http://localhost:5000/marks/${roll_number}`, function (data, status) {
    var details = data.data;


    var roll = dialogBox.querySelector('#roll')
    roll.value = details["rollNo"]
    roll.readOnly = true;

    var sname = dialogBox.querySelector('#sname')
    sname.value = details["name"]
    sname.readOnly = true;

    var year = dialogBox.querySelector('#admYear')
    year.readOnly = true;
    year.value = details["admissionYear"]

    var class_no = dialogBox.querySelector('#classNo')
    class_no.readOnly = true;
    class_no.value = details["classNo"]

    var table_details = "";
    tbody = dialogBox.querySelector("tbody")

    // Array to store subject IDs


    for (let i = 0; i < details["subjects"].length; i++) {
      var subjectId = details["subjects"][i]["subjectId"];

      subjectIds.push(subjectId);
      var mark = details["subjects"][i]["marks"]
      table_details +=
        `<tr>
          <td>${subjectId}</td>
          <td>${details["subjects"][i]["subjectName"]}</td>
          <td>
            ${(mark != null ?
          `<input type="number" value="${mark}" id="marks-${subjectId}" name="marks[]">` +
          `<input value="${subjectId}" type="hidden" name="subject_id[]">` :
          `<input type="number" placeholder="Enter marks" readOnly id="marks-${subjectId}" name="marks[]">
              <input value="${subjectId}" type="hidden" name="subject_id[]">`)}
          </td>
        </tr>`;
    }

    tbody.innerHTML = table_details;
    if (document.getElementById("edit-btn").hidden == false) {
      for (let i = 0; i < details["subjects"].length; i++) {
        document.getElementById(`marks-${details["subjects"][i]["subjectId"]}`).readOnly = true;
      }
    }

    document.getElementById("edit-btn").addEventListener("click", () => {
      if (document.getElementById("edit-btn").hidden == true) {
        for (let i = 0; i < details["subjects"].length; i++) {
          document.getElementById(`marks-${details["subjects"][i]["subjectId"]}`).readOnly = false;
        }
      }
    })

    get_all_students();
  });
}

function update_marks(subject_id) {
  subject_id = subjectIds
  const rollNo = document.getElementById("roll").value;
  const responseMessage = document.getElementById("response-message");

  const marks = []
  for (let i = 0; i < subject_id.length; i++) {
    let mark = document.getElementById(`marks-${subject_id[i]}`);
    marks.push(parseFloat(mark.value));
  }

  let jsonData = {
    "data": {
      "subjects": subject_id,
      "marks": marks
    }
  }

  jsonData = JSON.stringify(jsonData);

  $.ajax({
    type: "PUT",
    url: `http://localhost:5000/marks/` + rollNo,
    data: jsonData,
    contentType: "application/json",
    success: function (response) {
      responseMessage.textContent = response?.message;
      get_student(rollNo);
      document.getElementById("submit-btn").hidden = true;
      document.getElementById("edit-btn").hidden = false;
      document.getElementsByTagName("input").readOnly = true;
    },
    error: function (response) {
      errorMessage = ``;
      console.log(response.responseJSON)
      // response.responseJSON["error"].forEach(i => {
      //   console.log(i)
      //   errorMessage += parseString(i);
      // });
      const message = response.responseJSON.error;
      for (let i = 0; i < message.length; i++) {
        errorMessage += message[i];
      }
      responseMessage.innerText = errorMessage
    },
  })
}

{/* <td> 
            <button class='btn btn-primary btn-sm edit-btn-${details[i]["id"]}' onclick="dialogBox('put','${details[i]["id"]}')" style='margin:5px'>Edit</button>
            <button class='btn btn-danger btn-sm del-btn-${details[i]["id"]}' onclick='delete_student("${details[i]["id"]}")'>Delete</button>

          </td > */}
function makeDropdown() {
  $.get("http://localhost:5000/class", function (data, status) {
    var details = data.data;
    var droplist = `<option value="" disabled selected><i>Select a class</i></option>`;

    for (let i = 0; i < details.length; i++) {
      droplist =
        `${droplist}
        <option value='${details[i]["id"]}'>${details[i]["classNo"]}</option>
        `;
    }

    document.getElementById("classNo").innerHTML = droplist;
  });
}

function dialogBox(method, stuId = "") {

  document.getElementById("responseMessage").textContent = "";
  const add_dialog = document.getElementById("addDialog");
  const closeBtn = document.getElementById("closeBtn");

  const form = document.getElementById("stu-entry");
  form.setAttribute("data-method", method);
  form.setAttribute("data-stuId", stuId);

  if (method == 'get') {
    const marks_dialog = document.getElementById("marksheet");
    const closeBtn = marks_dialog.querySelector("#closeBtn");

    marks_dialog.querySelector('#entry-header').innerText = "Student Marksheet";
    marks_dialog.querySelector("#roll-label").innerText = "Roll Number:"
    marks_dialog.querySelector("#sname-label").innerText = "Name: ";
    marks_dialog.querySelector("#admYear-label").innerText = "Admission year: ";
    marks_dialog.querySelector("#classNo-label").innerText = "Class: ";

    const edit_button = document.getElementById("edit-btn")
    const submit_button = document.getElementById("submit-btn");

    edit_button.addEventListener("click", () => {
      submit_button.hidden = false;
      edit_button.hidden = true;
    })
    if (!marks_dialog.open) {
      marks_dialog.showModal();
    }

    closeBtn.addEventListener("click", () => {
      marks_dialog.close();
      submit_button.hidden = true;
      edit_button.hidden = false;
      document.getElementById("response-message").innerText = "";
    });


    get_student(stuId)
  }
  else if (method === "post") {

    document.getElementById("stu-entry").reset();
    document.getElementById('entry-header').innerHTML = "Student entry form";
    document.getElementById("sname-label").innerHTML = "Enter student name";
    document.getElementById("admYear-label").innerHTML = "Enter their admission year";
    document.getElementById("classNo-label").innerHTML = "Enter their class";
    makeDropdown();

    if (!add_dialog.open) {
      add_dialog.showModal();
    }

    closeBtn.addEventListener("click", () => {
      add_dialog.close();
    });

  }
  else if (method === "put") {

    document.getElementById("stu-entry").reset();
    document.getElementById('entry-header').innerHTML = "Student edit form";
    document.getElementById("sname-label").innerHTML = "Enter new student name";
    document.getElementById("admYear-label").innerHTML = "Enter their admission year";
    document.getElementById("classNo-label").innerHTML = "Enter their class";
    makeDropdown();

    if (!add_dialog.open) {
      add_dialog.showModal();
    }

    closeBtn.addEventListener("click", () => {
      add_dialog.close();
    });

  }
}


function submit_form() {
  const form = document.getElementById("stu-entry");
  let method = form.getAttribute("data-method");

  if (method === "post") {
    post_student();
  } else if (method === "put") {
    put_student();
  }
}

function post_student() {
  let form = document.getElementById("stu-entry");
  let responseMessage = document.getElementById("responseMessage");
  event.preventDefault();
  var selectElement = document.getElementById('classNo');

  var selectedOption = selectElement.options[selectElement.selectedIndex];
  var selectedValue = selectedOption.value;
  const stuData = {
    name: form.elements['sname'].value,
    admissionYear: parseFloat(form.elements['admYear'].value),
    classId: parseFloat(selectedValue)
  };

  const jsonData = JSON.stringify(stuData);

  $.ajax({
    type: "POST",
    url: "http://localhost:5000/students",
    data: jsonData,
    contentType: "application/json",
    success: function (response) {
      responseMessage.textContent = "Student added successfully: " + response?.message;
      get_all_students();
    },
    error: function (response) {

      errorMessage = ""
      if (response?.responseJSON?.name?.[0] != undefined) {
        errorMessage += response?.responseJSON?.name?.[0]
      }; if (response?.responseJSON?.admissionYear?.[0] != undefined) {
        errorMessage += " " + response?.responseJSON?.admissionYear?.[0];
      }; if (response?.responseJSON?.classNo?.[0] != undefined) {
        errorMessage += " " + response?.responseJSON?.classNo?.[0];
      };
      responseMessage.textContent = errorMessage
    },
  });

  setTimeout(function () {
    document.getElementById("sname").value = "";
    document.getElementById("admYear").value = "";
    document.getElementById("classNo").value = "";
  }, 1500);

  setTimeout(function () {
    document.getElementById("addDialog").close();
  }, 2000)
}

function put_student() {
  let form = document.getElementById("stu-entry");
  let responseMessage = document.getElementById("responseMessage");

  event.preventDefault();

  var selectElement = document.getElementById('classNo');
  var selectedOption = selectElement.options[selectElement.selectedIndex];
  var selectedValue = selectedOption.value;

  const stu_data = {
    name: form.elements['sname'].value,
    admissionYear: parseFloat(form.elements['admYear'].value),
    classNo: selectedValue
  };

  const json_data = JSON.stringify(stu_data);

  $.ajax({
    type: "PUT",
    url: "http://localhost:5000/students/" + form.getAttribute("data-stuId"),
    data: json_data,
    contentType: "application/json",
    success: function (response) {
      responseMessage.textContent = "Student edited successfully: " + response?.message;
      get_all_students();
    },
    error: function (response) {

      errorMessage = ""
      if (response?.responseJSON?.name?.[0] != undefined) {
        errorMessage += response?.responseJSON?.name?.[0]
      }; if (response?.responseJSON?.admissionYear?.[0] != undefined) {
        errorMessage += " " + response?.responseJSON?.admissionYear?.[0];
      }; if (response?.responseJSON?.classNo?.[0] != undefined) {
        errorMessage += " " + response?.responseJSON?.classAssigned?.[0];
      };
      responseMessage.textContent = errorMessage
    },
  });

  setTimeout(function () {
    document.getElementById("sname").value = "";
    document.getElementById("admYear").value = "";
    document.getElementById("classNo").value = "";
  }, 1500);

  setTimeout(function () {
    document.getElementById("addDialog").close();
  }, 2000)
}

function delete_student(rollNo) {
  $.ajax({
    type: "DELETE",
    url: "http://localhost:5000/students/" + rollNo,
    success: function (response) {
      get_all_students();
    },
    error: function (response) {
    }
  })
}

const apiRequest = {
  get: (url, params, successCallback, errorCallback) => {
    $.ajax({
      type: "PUT",
      url: url,
      data: json_data,
      contentType: "application/json",
      success: function (response) {
        successCallback && successCallback(response);
      },
      error: function (response) {
        errorCallback && errorCallback(response);
      },
    });
  }
}


function onSuccess (response) {
  responseMessage.textContent = "Student edited successfully: " + response?.message;
  get_all_students();
}

function onError() {
 
}

apiRequest.get("http://localhost:5000/students/" + form.getAttribute("data-stuId"),onSuccess, onError)