document.addEventListener('DOMContentLoaded', () => {

  populateTasks();

});

function populateTasks() {
  fetch(`/policorp/tasks/`)
  .then(response => response.json())
  .then(data => {
      data.forEach( function(task) {
        const option = document.createElement('a');
        option.classList.add('dropdown-item');
        option.dataset.taskid = task.id;
        option.innerHTML = task.name;
        document.querySelector('#taskDropdownMenu').append(option);
      });
  })
}
