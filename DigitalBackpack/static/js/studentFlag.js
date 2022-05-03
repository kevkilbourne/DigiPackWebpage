// import models from django.db;

function swapFlag(event, element)
{
  if (element.className == "notFlagged")
  {
    element.className = "flagged";

    alert("Student has been successfully flagged.");

    let teachInput = prompt("Would you like to send an email to the student's parents/guardians (yes or no)?").toLowerCase();

    switch (teachInput)
    {
      case "yes":
        window.open('https://mail.google.com/mail/?view=cm&fs=1','_blank');
        break;

      case "no":
        break;

      default:
        break;
    }

    return element;
  }

  else
  {
    element.className = "notFlagged";

    // prompt user that it was successful
    alert("Student has been successfully unflagged.");

    return element;
  }
}
