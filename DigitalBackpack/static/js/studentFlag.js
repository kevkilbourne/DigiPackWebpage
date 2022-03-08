var button = document.querySelectorAll('button');

button.forEach(button =>
  {
    button.addEventListener('click', () => swapFlag(button.id));
  });

function swapFlag(studentID)
{
    // change ID from "notFlagged" to "flagged"
    if (studentID == "flagged")
    {
      // change id value
      studentID = "notFlagged";

      // prompt user that it was successful
      alert("Student has been successfully unflagged.");

      window.addEventListener('load', (event) => {
        console.log('page is fully loaded');
      });

      return studentID;
    }

    else if (studentID == "notFlagged")
    {
      // change id value
      studentID = "flagged";

      // prompt user that it was successful
      alert("Student has been successfully flagged.");

      window.addEventListener('load', (event) => {
        console.log('page is fully loaded');
      });

      return studentID;
    }
}
