document.addEventListener('DOMContentLoaded', () => {

  loadFilters();
  document.querySelector('#locationScheduleContainer').style.display = 'block';
  document.querySelector('#locationConfigurationContainer').style.display = 'none';
  document.querySelector('#location-schedule-link').addEventListener('click', () => handleLocationScheduleLinkClick());
  document.querySelector('#location-config-link').addEventListener('click', () => handleLocationConfigurationLinkClick());
  document.querySelector('#lookupBookingsButton').addEventListener('click', (event) => handleSearchClick(event));
  document.querySelector('#createSingleAvailabilityButton').addEventListener('click', () => handleCreateAvailabilityClick());
  document.querySelector('#configExtendCheck').addEventListener('click', (event) => handleExtendClick(event));
  document.querySelector('#configRepeatDaysCheck').addEventListener('click', (event) => handleRepeatDaysClick(event));

});

// ********************************
// *** EVENT HANDLERS Functions ***
// ********************************

// *** NAVBAR EVENTS ***

function handleLocationScheduleLinkClick() {
  document.querySelector('#locationScheduleContainer').style.display = 'block';
  document.querySelector('#locationConfigurationContainer').style.display = 'none';
}

function handleLocationConfigurationLinkClick() {

  clearNode(document.querySelector('#configLocationDropdownMenu'));
  populateLocations(document.querySelector('#configLocationDropdownMenu'), handleConfigLocationSelectionClick);
  clearNode(document.querySelector('#configTaskDropdownMenu'));
  populateTasks(document.querySelector('#configTaskDropdownMenu'));

  document.querySelector('#locationScheduleContainer').style.display = 'none';
  document.querySelector('#locationConfigurationContainer').style.display = 'block';
}

// *** SCHEDULE EVENTS ***

function handleLocationSelectionClick(event) {

  const dropdownLocationButton = document.querySelector('#dropdownLocationButton');
  dropdownLocationButton.innerHTML = event.currentTarget.innerHTML;
  dropdownLocationButton.dataset.locationid = event.currentTarget.dataset.locationid;

  const lookupBookingsButton = document.querySelector('#lookupBookingsButton');
  lookupBookingsButton.style.cursor = 'pointer';
  lookupBookingsButton.disabled = false;

}

function handleSearchClick(event) {
  dropdownLocationButton = document.querySelector('#dropdownLocationButton');

  const date = new Date($datepicker.value());

  const url = constructUrlLocationSchedule(dropdownLocationButton.dataset.locationid, date);

  fetch(url)
  .then(response => response.json())
  .then(data => {

      console.log(data);
      const list = document.querySelector('#locationSchedule');
      clearNode(list);
      const listHeading = document.createElement('h5');
      if (data.length === 0) {listHeading.innerHTML = 'No Bookings';}
      else { listHeading.innerHTML = 'Bookings';}
      list.append(listHeading);
      data.forEach( (bookingData)  => {
        element = createBooking(bookingData);
        list.append(element);
      });
      list.style.display = 'block';
  })
}

// *** CONFIGURATION EVENTS ***

function handleConfigLocationSelectionClick(event) {

  const dropdownConfigLocationButton = document.querySelector('#configLocationDropdownButton');
  dropdownConfigLocationButton.innerHTML = event.currentTarget.innerHTML;
  dropdownConfigLocationButton.dataset.locationid = event.currentTarget.dataset.locationid;

  evaluateCreateSingleAvailabilityState();
}

function handleConfigTaskSelectionClick(event) {

  const dropdownConfigTaskButton = document.querySelector('#configTaskDropdownButton');
  dropdownConfigTaskButton.innerHTML = event.currentTarget.innerHTML;
  dropdownConfigTaskButton.dataset.taskid = event.currentTarget.dataset.taskid;
  dropdownConfigTaskButton.dataset.duration = event.currentTarget.dataset.duration;

  evaluateCreateSingleAvailabilityState();

}

function handleExtendClick(event) {
  const checkbox = event.currentTarget;
  const container = document.querySelector('#configUntilTimepickerContainer');
  if (checkbox.checked == true){
    container.classList.remove('d-none');
    container.classList.add('d-flex');
  } else {
    container.classList.remove('d-flex');
    container.classList.add('d-none');
  }
}

function handleRepeatDaysClick(event) {
  const checkbox = event.currentTarget;
  const containerDays = document.querySelector('#daysOfWeekContainer');
  const containerUntilDate = document.querySelector('#configUntilDatepickerContainer');
  if (checkbox.checked == true){
    containerDays.classList.remove('d-none');
    containerDays.classList.add('d-inline-flex');
    containerUntilDate.classList.remove('d-none');
    containerUntilDate.classList.add('d-flex');
  } else {
    containerDays.classList.remove('d-inline-flex');
    containerDays.classList.add('d-none');
    containerUntilDate.classList.remove('d-flex');
    containerUntilDate.classList.add('d-none');
  }
}

function handleCreateAvailabilityClick() {

  // if user is not logged in, then redirect to login page
  if (username === "") {
    window.location.href = loginurl;
  } else {

    const locationid = document.querySelector('#configLocationDropdownButton').dataset.locationid;
    const taskid = document.querySelector('#configTaskDropdownButton').dataset.taskid;
    const taskduration = document.querySelector('#configTaskDropdownButton').dataset.duration;
    let when = new Date(`${$configDatepicker.value()}`);
    when.setHours($configTimepicker.value().substring(0, 2));
    when.setMinutes($configTimepicker.value().substring(3, 5));

    const extendCheck = document.querySelector('#configExtendCheck');
    let untilTime = null;
    if (extendCheck.checked == true) { untilTime = $configUntilTimepicker.value(); }
    let configs;
    try {
      configs = createAvailabilitiesJsonData(locationid, taskid, taskduration, when, untilTime);
    }
    catch (error) {
      showMessage('Error', `There was an error generating the availability configuration data: ${error}`);
      return;
    }

    const repeatDaysCheck = document.querySelector('#configRepeatDaysCheck');
    let days = [false, false, false, false, false, false, false];
    let untilDate = null;
    if (repeatDaysCheck.checked == true) {
      untilDate = new Date(`${$configUntilDatepicker.value()}`);
      const container = document.querySelector('#daysOfWeekContainer');
      let i = 0;
      while (i < days.length) {
        button = container.children[i];
        if (button.nodeType === 1) {
          if (button.getAttribute("aria-pressed") === "true") days[i] = true;
          i++;
        }
      }
    }
    try {
      configs = appendNewAvailabilityDatesToJsonData(configs, days, when, untilDate);
    }
    catch (error) {
      showMessage('Error', `There was an error generating the availability configuration data: ${error}`);
      return;
    }

    fetch(`/policorp/createavailabilities/`, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrftoken },
      mode: 'same-origin',
      body: JSON.stringify(configs)
    })
    .then(response => response.json())
    .then(data => {
      console.log('Create availabilities response');
      console.log(data);
      return getAvailabilitiesResponseErrors(data);
    })
    .then(errors => {
      if (errors === 0) {
        showMessage('Success', `You have successfully created an abailability configuration`);
      } else {
        showMessage('Error', `There were ${errors} errors creating the abailability configuration`);
      }
    });
    handleLocationScheduleLinkClick();
  }
}

// ***************************
// *** AUXILIARY Functions ***
// ***************************

function loadFilters() {

  populateLocations(document.querySelector('#locationDropdownMenu'), handleLocationSelectionClick);

  document.querySelector('#locationSelector').style.display = 'block';
  document.querySelector('#locationSchedule').style.display = 'none';

}

function populateLocations(dropDown, clickHandler) {
  fetch(`/policorp/mysupervisedlocations/`)
  .then(response => response.json())
  .then(data => {
      data.forEach( function(location) {
        const option = document.createElement('a');
        option.classList.add('dropdown-item');
        option.id = 'locationOption';
        option.dataset.locationid = location.id;
        option.innerHTML = location.name;
        option.addEventListener('click', (event) => clickHandler(event));

        dropDown.append(option);
      });
  })
}

function populateTasks(dropDown) {
  fetch(`/policorp/tasks/`)
  .then(response => response.json())
  .then(data => {
      data.forEach( function(task) {
        const option = document.createElement('a');
        option.classList.add('dropdown-item');
        option.id = 'taskOption';
        option.dataset.taskid = task.id;
        option.dataset.duration = task.duration;
        option.innerHTML = `${task.name} (${toFormattedDuration(task.duration)})`;
        option.addEventListener('click', (event) => handleConfigTaskSelectionClick(event));

        dropDown.append(option);
      });
  })
}

function constructUrlLocationSchedule(locationid, date) {
  return `/policorp/locationschedule/${locationid}/${date.getFullYear()}${date.getMonth() + 1}${date.getDate()}`
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
  whenContainer.innerHTML = toFormattedTime(new Date(Date.parse(data.availability.when)));
  aInfo.append(whenContainer);

  // WHAT
  const whatContainer = document.createElement('div');
  whatContainer.innerHTML = data.availability.what.name;
  aInfo.append(whatContainer);

  // WHO
  const whoContainer = document.createElement('div');
  whoContainer.innerHTML = data.username;
  aInfo.append(whoContainer);

  return a;
}

function clearNode(node) {
  var children = Array.from(node.children);
  if (children !== undefined) { children.forEach((child) => { child.remove(); }) };
  node.innerHTML = '';
}

function toFormattedTime(datetimeObj) {
  timeFrom = datetimeObj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true });
  return (timeFrom);
}

function toFormattedDuration(duration) {
  if (duration < 60) {
    return `${duration} min`;
  } else {
    const hours = Math.floor(duration / 60);
    const minutes = duration % 60;
    if (minutes !== 0) { return `${hours} hs ${minutes} min`; }
    else { return `${hours} hs`; }
  }
}

function addMinutes(dt, minutes) {
    return new Date(dt.getTime() + minutes*60000);
}

function evaluateCreateSingleAvailabilityState() {
  const location = document.querySelector('#configLocationDropdownButton');
  const task = document.querySelector('#configTaskDropdownButton');
  const button = document.querySelector('#createSingleAvailabilityButton');

  if ((!isNaN(location.dataset.locationid)) && (!isNaN(task.dataset.taskid))) {
    button.disabled = false;
    button.style.cursor = 'pointer';
  }
}

function showMessage(title, message) {
  document.querySelector('#messageModalLabel').innerHTML = title;
  document.querySelector('#messageModalBody').innerHTML = message;
  $("#messageModal").modal('show');
}

function createAvailabilitiesJsonData(locationid, taskid, taskduration, when, untilTime) {

  let json = [{
              "locationid": locationid,
              "taskid": taskid,
              "when": encodeDateTime(when)
          }];

  if (untilTime !== null) {
    let until = new Date(when);
    until.setHours(untilTime.substring(0, 2));
    until.setMinutes(untilTime.substring(3, 5));

    if (until < when) throw "Invalid time settings";

    newWhenBegin = addMinutes(when, taskduration);
    newWhenEnd = addMinutes(newWhenBegin, taskduration);

    while (newWhenEnd <= until) {
      json.push({
                "locationid": locationid,
                "taskid": taskid,
                "when": encodeDateTime(newWhenBegin)
                });

      newWhenBegin = addMinutes(newWhenBegin, taskduration);
      newWhenEnd = addMinutes(newWhenBegin, taskduration);
    }
  }

  return json;
}

function appendNewAvailabilityDatesToJsonData(initialAvailabilityJson, days, fromDate, untilDate) {

  let json = JSON.parse(JSON.stringify(initialAvailabilityJson));
  let currentDate = new Date();
  currentDate.setDate(fromDate.getDate() + 1);
  currentDate.setHours(0, 0, 0, 0);
  while (currentDate <= untilDate) {
    if (days[currentDate.getDay()] === true) {
      initialAvailabilityJson.forEach(a => {
        let newWhen = decodeDateTime(a["when"]);
        newWhen.setDate(currentDate.getDate());
        newWhen.setMonth(currentDate.getMonth());
        newWhen.setFullYear(currentDate.getFullYear());
        json.push({
                  "locationid": a["locationid"],
                  "taskid": a["taskid"],
                  "when": encodeDateTime(newWhen)
                  });
      });
    }
    currentDate.setDate(currentDate.getDate() + 1);
  }

  return json;
}

function getAvailabilitiesResponseErrors(response) {
  let errorCount = 0;

  response.forEach(r => { if (r.error) { errorCount++; } });

  return errorCount;
}

function encodeDateTime(datetime) {
  return datetime.toISOString().replace("Z", "+00:00");
}

function decodeDateTime(datetimestring) {
  return new Date(datetimestring.replace("+00:00", "Z"));
}
