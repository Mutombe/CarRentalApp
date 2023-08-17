// Get all the options
var options = document.querySelectorAll('.option');

// Add click event listeners to the options
for (var i = 0; i < options.length; i++) {
  options[i].addEventListener('click', function(e) {
    e.preventDefault();
    // Get the target data attribute
    var target = this.getAttribute('data-target');
    // Hide all the content elements
    var content = document.querySelectorAll('.content > div');
    for (var j = 0; j < content.length; j++) {
      content[j].classList.remove('active');
    }
    // Show the content element with the corresponding target
    var element = document.getElementById(target);
    element.classList.add('active');
    // Set the active class on the clicked option
    var activeOption = document.querySelector('.option.active');
    activeOption.classList.remove('active');
    this.classList.add('active');
  });
}