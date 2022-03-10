function swapFlag(event, element)
{
    // change ID from "notFlagged" to "flagged"
    if (element.className == "flagged")
    {
      // change id value
      element.className = "notFlagged";

      // prompt user that it was successful
      alert("Student has been successfully unflagged.");

      return element;
    }

    else if (element.className == "notFlagged")
    {
      // change id value
      element.className = "flagged";

      // prompt user that it was successful
      alert("Student has been successfully flagged.");

      return element;
    }
}
