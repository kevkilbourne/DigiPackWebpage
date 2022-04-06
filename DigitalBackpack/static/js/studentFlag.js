/*
For Views.py
def landing_page(request):
    return render(request, 'DigitalBackpack/sendEmail.html')
*/

function swapFlag(event, element)
{
  if (element.className == "notFlagged")
  {
    let teacherInput = prompt("What level would you like to flag the student, 1 or 2?");

    switch (teacherInput)
    {
      case "1":
        // change id value
        element.className = "flaggedlvl1";

        // prompt user that it was successful
        alert("Student has been successfully flagged to level 1 (base).");

        break;

      case "2":
        // change id value
        element.className = "flaggedlvl2";

        // prompt user that it was successful
        alert("Student has been successfully flagged to level 2 (severe).");

        let teachInput = prompt("Would you like to send an email, text, both, or none?").toLowerCase();

        switch (teachInput)
        {
          case "email":
            let userEmail = prompt("Write your message here.");

            sendEmail(sendTo, sendFrom, userEmail);
            break;

          case "text":
            let userText = prompt("Write your message here.");

            sendText(sendTo, sendFrom, userText);
            break;

          case "both":
            let userMessage = prompt("Write your message here.");

            sendEmail(sendTo, sendFrom, userMessage);
            sendText(sendTo, sendFrom, userMessage);
            break;

          case "none":
            break;

          default:
            break;
        }

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

function sendEmail(sendTo, sendFrom, message)
{
  Email.send(
    {
      Host: "www.gmail.com",
      Username: "",
      Password: "",
      To: sendTo,
      From: sendFrom,
      Subject: "test",
      Body: message,
    })
    .then(function (message)
    {
      alert("Email sent successfully");
    });
}

function sendText(sendTo, sendFrom, message)
{
  return ;
}
