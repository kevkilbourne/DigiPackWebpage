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

    switch (teachInput)
    {
      case "1":
        // change id value
        element.className = "flaggedlvl1";

        // prompt user that it was successful
        alert("Student has been successfully flagged to level 1 (base).");

        return element;
        break;

      case "2":
        // change id value
        element.className = "flaggedlvl2";

        // prompt user that it was successful
        alert("Student has been successfully flagged to level 2 (severe).");

        let teacherInput = prompt("Would you like to send an email, text, both, or none?");

          switch (teachInput)
          {
            case "email":
              sendEmail(sendTo, sendFrom, message);
              break;

            case "text":
              sendText(sendTo, sendFrom, message);
              break;

            case "both":
              sendEmail(sendTo, sendFrom, message);
              sendText(sendTo, sendFrom, message);
              break;

            case "none":
              break;

            default:
              break;
          }

        return element;
        break;

      default:
        break;
    }
  }

  else
  {
    element.className = "notFlagged";

    // prompt user that it was successful
    alert("Student has been successfully unflagged.");

    return element;
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
      alert("Email sent successfully")
    });
}
