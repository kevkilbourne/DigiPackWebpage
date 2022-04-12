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