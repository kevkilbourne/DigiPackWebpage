/*
For Views.py
def landing_page(request):
    return render(request, 'DigitalBackpack/sendEmail.html')
*/

function swapFlag(event, element)
{
  if (element.className == "notFlagged")
  {
    element.className = "flagged";

    alert("Student has been successfully flagged.");

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
