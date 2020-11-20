document.addEventListener('DOMContentLoaded', () => {

  populateTasks();

});

// ********************************
// *** EVENT HANDLERS Functions ***
// ********************************

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
        element = createAvailability(availabilityData, false);
        document.querySelector('#availabilityList').append(element);
      });
  })
}

function handleBookClick(event) {

  // if user is not logged in, then redirect to login page
  if (username === "") {
    window.location.href = loginurl;
  } else {
    fetch(`/policorp/book/${event.currentTarget.dataset.availabilityid}`, {
    method: 'POST',
    headers: {'X-CSRFToken': csrftoken},
    mode: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);

        // TODO: redirect to my Schedule
        });
    }
}

// ***************************
// *** AUXILIARY Functions ***
// ***************************

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

function createAvailability(data, booked) {
  // create availability container
  a = document.createElement('div');
  a.id = 'availability';
  a.dataset.availabilityid = data.id;
  a.className = 'container p-3 my-3 border d-flex flex-row justify-content-between align-items-center';

  // create availability info container
  const aInfo = document.createElement('div');
  aInfo.id = 'availabilityInfo';
  a.append(aInfo);

  // WHEN
  const whenContainer = document.createElement('div');
  whenContainer.innerHTML = toFormattedDateTime(new Date(Date.parse(data.when)));
  aInfo.append(whenContainer);

  // WHERE
  const whereContainer = document.createElement('div');
  whereContainer.innerHTML = data.where.name;
  aInfo.append(whereContainer);

  // create action button whenContainer
  const aAction = document.createElement('div');
  aAction.id = 'availabilityAction';
  a.append(aAction);

  // action dropdownMenuButton
  const aActionButton = document.createElement('button');
  aActionButton.id = 'availabilityActionButton';
  aActionButton.dataset.availabilityid = data.id;
  if (booked) {
    aActionButton.className = 'btn btn-danger';
    aActionButton.innerHTML = 'Cancel';
    // TODO: Add Cancel booking click event handler
  }
  else {
    aActionButton.className = 'btn btn-primary';
    aActionButton.innerHTML = 'Book';
    aActionButton.addEventListener('click', (event) => { handleBookClick(event); });
  }

  aAction.append(aActionButton);

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
