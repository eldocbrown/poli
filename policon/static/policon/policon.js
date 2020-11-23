document.addEventListener('DOMContentLoaded', () => {

  if (username !==   "") document.querySelector('#my-schedule-link').addEventListener('click', () => loadMySchedule());

  loadAvailabilities();

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
        if (!data.error) {
          const task = data.availability.what.name;
          const datetime = toFormattedDateTime(new Date(Date.parse(data.availability.when)));
          showMessage('Booking confirmed', `You have successfully booked the task ${task} on ${datetime}`);
        } else {
          console.error(data);
        }

        loadMySchedule()
        });
    }
}

function handleCancelClick(event) {
  fetch(`/policorp/cancelbooking/${event.currentTarget.dataset.bookingid}`, {
  method: 'POST',
  headers: {'X-CSRFToken': csrftoken},
  mode: 'same-origin'
  })
  .then(response => response.json())
  .then(data => {
      if (!data.error) {
        const task = data.availability.what.name;
        const datetime = toFormattedDateTime(new Date(Date.parse(data.availability.when)));
        showMessage('Booking cancelled', `You have successfully cancelled the task ${task} on ${datetime}`);
      } else {
        console.error(data);
      }

      loadMySchedule()
  });
}

// ***************************
// *** AUXILIARY Functions ***
// ***************************

function loadAvailabilities() {

  populateTasks();

  document.querySelector('#availabilitySelector').style.display = 'block';
  document.querySelector('#mySchedule').style.display = 'none';
}

function loadMySchedule() {

  const sectionContent = document.querySelector('#mySchedule');
  clearNode(sectionContent);
  heading = document.createElement('h5');
  heading.innerHTML = 'My Schedule';
  sectionContent.append(heading);

  populateSchedule();

  document.querySelector('#availabilitySelector').style.display = 'none';
  sectionContent.style.display = 'block';
}

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

        option.addEventListener('click', (event) => handleTaskSelectionClick(event));

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
  aActionButton.className = 'btn btn-primary';
  aActionButton.innerHTML = 'Book';
  aActionButton.addEventListener('click', (event) => handleBookClick(event));

  aAction.append(aActionButton);

  return a;
}

function populateSchedule() {
  fetch(`/policorp/myschedule/`)
  .then(response => response.json())
  .then(data => {
      data.forEach( (booking) => document.querySelector('#mySchedule').append(createBooking(booking)));
  })
}

function createBooking(data) {
  // create booking container
  a = document.createElement('div');
  a.id = 'booking';
  a.dataset.bookingid = data.id;
  a.className = 'container p-3 my-3 border d-flex flex-row justify-content-between align-items-center';

  // create availability info container
  const aInfo = document.createElement('div');
  aInfo.id = 'bookingInfo';
  a.append(aInfo);

  // WHEN
  const whenContainer = document.createElement('div');
  whenContainer.innerHTML = toFormattedDateTime(new Date(Date.parse(data.availability.when)));
  aInfo.append(whenContainer);

  // WHAT
  const whatContainer = document.createElement('div');
  whatContainer.innerHTML = data.availability.what.name;
  aInfo.append(whatContainer);

  // WHERE
  const whereContainer = document.createElement('div');
  whereContainer.innerHTML = data.availability.where.name;
  aInfo.append(whereContainer);

  // create action button whenContainer
  const aAction = document.createElement('div');
  aAction.id = 'bookingAction';
  a.append(aAction);

  // action dropdownMenuButton
  const aActionButton = document.createElement('button');
  aActionButton.id = 'bookingActionButton';
  aActionButton.dataset.bookingid = data.id;
  aActionButton.className = 'btn btn-danger';
  aActionButton.innerHTML = 'Cancel';
  aActionButton.addEventListener('click', (event) => handleCancelClick(event));

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
  time = datetimeObj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true });
  return (dayOfWeek + ', ' + month + ' ' + date + ' at ' + time);
}

function showMessage(title, message) {
  document.querySelector('#messageModalLabel').innerHTML = title;
  document.querySelector('#messageModalBody').innerHTML = message;
  $("#messageModal").modal('show');
}
