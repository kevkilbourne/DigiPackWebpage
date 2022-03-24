/*
For Views.py
def landing_page(request):
    return render(request, 'DigitalBackpack/sendEmail.html')
*/

function swapFlag(event, element)
{
  if (element.className == "notFlagged")
  {
    // change id value
    element.className = "flaggedlvl1";

    // prompt user that it was successful
    alert("Student has been successfully flagged to level 1 (base).");

    return element;
  }

    // change ID from "flaggedlvl1" to "flaggedlvl2"
    else if (element.className == "flaggedlvl1")
    {
      // change id value
      element.className = "flaggedlvl2";

      // prompt user that it was successful
      alert("Student has been successfully flagged to level 2 (intermediate).");

      let teachInput = prompt("Would you like to send this students parents an email? (yes or no)").toLowerCase();

      switch (teachInput)
      {
        case "yes":
          // send to message page to send email
          console.log("lvl 2 email");
          let sendTo = prompt("Who is the email going to?");
          console.log(sendTo);
          let sendFrom = prompt("What is your email?");
          console.log(sendFrom);
          let message = prompt("Write your message below.");
          console.log(message);

          sendEmail(sendTo, sendFrom, message);
          break;

        case "no":
          break;

        default:
          break;
      }

      return element;
    }

    // change ID from "flaggedlvl2" to "flaggedlvl3"
    else if (element.className == "flaggedlvl2")
    {
      // change id value
      element.className = "flaggedlvl3";

      // prompt user that it was successful
      alert("Student has been successfully flagged to level 3 (severe).");

      let teachInput = prompt("Would you like to send this students parents a text? (yes or no)").toLowerCase();

      switch (teachInput)
      {
        case "yes":
          // send to message page to send email
          console.log("lvl 3 email");
          let sendTo = prompt("Who is the text going to?");
          console.log(sendTo);
          let sendFrom = prompt("What is your numer?");
          console.log(sendFrom);
          let message = prompt("Write your message below.");
          console.log(message);

          // sendEmail(sendTo, sendFrom, message);
          break;

        case "no":
          break;

        default:

      }

      return element;
    }

    // change ID from "flaggedlvl3" to "notFlagged"
    else if (element.className == "flaggedlvl3")
    {
      // change id value
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
      Username: "nmc288@nau.edu",
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
