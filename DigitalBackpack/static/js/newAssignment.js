
var deleteButtons = document.getElementsByClassName("delete");
let index;

for(index = 0; index < deleteButtons.length; index++) {
	console.log(deleteButtons[index]);
	deleteButtons[index].addEventListener("click", function() {
		this.parentElement.innerHtml = "";
	});
}

function deleteResource(event, element) {
	console.log("deleting Resource");
	element.parentElement.remove();
}
