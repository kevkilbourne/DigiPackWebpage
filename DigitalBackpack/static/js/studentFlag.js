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

    // change ID from "notFlagged" to "flagged"
    else if (element.className == "flaggedlvl1")
    {
      // change id value
      element.className = "flaggedlvl2";

      // prompt user that it was successful
      alert("Student has been successfully flagged to level 2 (intermediate).");

      return element;
    }

    // change ID from "notFlagged" to "flagged"
    else if (element.className == "flaggedlvl2")
    {
      // change id value
      element.className = "flaggedlvl3";

      // prompt user that it was successful
      alert("Student has been successfully flagged to level 3 (severe).");

      return element;
    }

    // change ID from "notFlagged" to "flagged"
    else if (element.className == "flaggedlvl3")
    {
      // change id value
      element.className = "notFlagged";

      // prompt user that it was successful
      alert("Student has been successfully unflagged.");

      return element;
    }
}
