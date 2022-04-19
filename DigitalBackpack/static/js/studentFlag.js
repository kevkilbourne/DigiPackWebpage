import models from django.db;

function swapFlag(event, element)
{
  if (element.className == "notFlagged")
  {
    element.className = "flagged";
/*
    Model.objects.filter(id = notFlagged).update(field1 = flagged);

    Student.flagged = "flagged";
    Student.save();

*/
    alert("Student has been successfully flagged.");

    let teachInput = prompt("Would you like to send an email to the student's parents/guardians (yes or no)?").toLowerCase();

    switch (teachInput)
    {
      case "yes":
        let sendTo = prompt("Who is this email going to (ex: john.doe@gmail.com)?");
        let userMessage = prompt("Write your email's message here.");

        sendEmail(sendTo, userEmail);
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
/*
    Model.objects.filter(id = flagged).update(field1 = notFlagged);

    Student.flagged = "notFlagged";
    Student.save();

*/
    // prompt user that it was successful
    alert("Student has been successfully unflagged.");

    return element;
  }
}

function sendEmail(sendTo, message)
{
  Email.send(
    {
      Host: "www.gmail.com",
      Username: "",
      Password: "",
      To: sendTo,
      From: User.objects.get(id=request.session.get('_auth_user_id')).email,
      Subject: "Regarding Your Students Activity in Class",
      Body: message,
    })
    .then(function (message)
    {
      alert("Email sent successfully");
    });
}
