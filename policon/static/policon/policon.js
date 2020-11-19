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
        option.id = 'taskOption';
        option.dataset.taskid = task.id;
        option.innerHTML = task.name;

        option.addEventListener('click', (event) => {
          handleTaskSelectionClick(event);
        });

        document.querySelector('#taskDropdownMenu').append(option);
      });
  })
}

function handleTaskSelectionClick(event) {

  taskid = event.currentTarget.dataset.taskid;

  document.querySelector('#dropdownTaskButton').innerHTML = event.currentTarget.innerHTML;

  fetch(`/policorp/availabilities/${taskid}`)
  .then(response => response.json())
  .then(data => {
      const list = document.querySelector('#availabilityList');
      clearNode(list);
      const listHeading = document.createElement('h5');
      listHeading.innerHTML = 'Available Openings'
      list.append(listHeading);

      data.forEach( (availabilityData)  => {
        element = createAvailability(availabilityData)
        document.querySelector('#availabilityList').append(element);

        // TODO: Handle availability reservation
      });
  })
}

function createAvailability(data) {
  // create availability container
  const a = document.createElement('div');
  a.id = 'availability';
  a.dataset.availabilityid = data.id;
  a.className = 'container p-3 my-3 border';

  // WHEN
  const whenContainer = document.createElement('div');
  whenContainer.innerHTML = toFormattedDateTime(new Date(Date.parse(data.when)));
  a.append(whenContainer);

  // WHERE
  const whereContainer = document.createElement('div');
  whereContainer.innerHTML = data.where.name;
  a.append(whereContainer);

  return a;
}

function clearNode(node) {
  var children = Array.from(node.children);
  if (children !== undefined) { children.forEach((child) => { child.remove(); }) };
  node.innerHTML = '';
}

function toFormattedDateTime(datetimeObj) {
  const locale = 'en-US';
  dayOfWeek = datetimeObj.toLocaleString(locale, { weekday: "long" });
  month = datetimeObj.toLocaleString(locale, { month: "long" });
  date = datetimeObj.getDate();
  time = datetimeObj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });
  return (dayOfWeek + ', ' + month + ' ' + date + ' at ' + time);
}
