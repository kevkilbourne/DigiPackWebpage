
//let form_count = Number($("[name=extraFieldCount]").val());
// get extra form count so we know what index to use for the next item.

function addInput() {
    let form_count = Number(document.getElementsByName("extraFieldCount")[0].value);
    form_count++;
    console.log(form_count);

    const element = document.createElement("input");
    element.setAttribute("type", "email");
    element.setAttribute("name", "email_" + form_count);
    document.getElementById("addStudentForm").append(element);
    // build element and append it to our forms container

    document.getElementsByName("extraFieldCount")[0].value = form_count;
    // increment form count so our view knows to populate 
    // that many fields for validation
}

