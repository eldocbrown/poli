import { createAvailabilitiesJsonData, appendNewAvailabilityDatesToJsonData } from './availabilities.js'
import { createActionButton } from './createActionButton.js'
import { addMinutes } from './dateTimeUtils.js'
import { getDateFromDatePickerValue } from './gijgoComponentUtils.js'

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
  const dropdownLocationButton = document.querySelector('#dropdownLocationButton');

  let date = "";
  if ($datepicker.value() !== "") {
    date = getDateFromDatePickerValue($datepicker.value(), localeGijGoComponent)
  }
  else {
    showMessage('Error', gettext('Invalid Date'));
    return;
  }

  searchSchedule(date);
}

function handleScheduleFilterClick(event) {

  const filter = event.detail.type;
  const all = document.querySelectorAll('#booking, #availability');
  const bookings = document.querySelectorAll('#booking');
  const availabilities = document.querySelectorAll('#availability');

  switch(filter) {
  case 'scheduleFilterAll':
    all.forEach((item, i) => {
      item.classList.remove('d-none');
      item.classList.add('d-flex');
    });
    break;
  case 'scheduleFilterBooked':
    bookings.forEach((item, i) => {
      item.classList.remove('d-none');
      item.classList.add('d-flex');
    });
    availabilities.forEach((item, i) => {
      item.classList.remove('d-flex');
      item.classList.add('d-none');
    });
    break;
  case 'scheduleFilterAvailable':
    bookings.forEach((item, i) => {
      item.classList.remove('d-flex');
      item.classList.add('d-none');
    });
    availabilities.forEach((item, i) => {
      item.classList.remove('d-none');
      item.classList.add('d-flex');
    });
    break;
  default:
    console.log('Unrecognized schedule filter');
  }
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
    let when = new Date(`${getDateFromDatePickerValue($configDatepicker.value(), localeGijGoComponent)}`);
    when.setHours($configTimepicker.value().substring(0, 2));
    when.setMinutes($configTimepicker.value().substring(3, 5));

    const extendCheck = document.querySelector('#configExtendCheck');
    let untilDateTime = null;
    if (extendCheck.checked == true) {
      const untilTime = $configUntilTimepicker.value()
      untilDateTime = new Date(when)
      untilDateTime.setHours(untilTime.substring(0,2), untilTime.substring(3,5))
    }
    let configs;
    try {
      configs = createAvailabilitiesJsonData(locationid, taskid, taskduration, when, untilDateTime, encodeDateTime);
    }
    catch (error) {
      showMessage('Error', gettext('There was an error generating the availability configuration data') + `: ${error}`);
      return;
    }

    const repeatDaysCheck = document.querySelector('#configRepeatDaysCheck');
    let days = [false, false, false, false, false, false, false];
    let untilDate = null;
    if (repeatDaysCheck.checked == true) {
      untilDate = new Date(`${getDateFromDatePickerValue($configUntilDatepicker.value(), localeGijGoComponent)}`);
      const container = document.querySelector('#daysOfWeekContainer');
      let i = 0;
      while (i < days.length) {
        const button = container.children[i];
        if (button.nodeType === 1) {
          if (button.getAttribute("aria-pressed") === "true") days[i] = true;
          i++;
        }
      }
    }
    try {
      configs = appendNewAvailabilityDatesToJsonData(configs, days, when, untilDate, encodeDateTime, decodeDateTime);
    }
    catch (error) {
      showMessage('Error', gettext('There was an error generating the availability configuration data') + `: ${error}`);
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
      return getAvailabilitiesResponseErrors(data);
    })
    .then(errors => {
      if (errors === 0) {
        showMessage(gettext('Success'), gettext('You have successfully created an availability configuration'));
      } else {
        showMessage('Error', gettext('There were') + ` ${errors} ` + gettext('errors creating the availability configuration'));
      }
    });
    handleLocationScheduleLinkClick();
  }
}

function handleCancelBookingClick(event) {
  const bookingId = event.currentTarget.dataset.dataId;
  const successMsgTitle = gettext('Booking cancelled');
  const successMsgBody = gettext('You have successfully cancelled the booking')
  fetch(`/policorp/cancelbooking/${bookingId}/`, {
    method: 'POST',
    headers: {'X-CSRFToken': csrftoken},
    mode: 'same-origin'
  })
  .then(response => {
    if (response.status === 201) {
      showMessage( successMsgTitle, successMsgBody);
      searchSchedule(getDateFromDatePickerValue($datepicker.value(), localeGijGoComponent));
    }
    else {
      throw response.error;
    }
  })
  .catch((error) => {
    console.error('Error:', error);
  });
}

function handleCancelAvailabilityClick(event) {
  const availabilityId = event.currentTarget.dataset.dataId;
  const successMsgTitle = gettext('Availability cancelled');
  const successMsgBody = gettext('You have successfully cancelled the availability')
  fetch(`/policorp/availability/${availabilityId}/`, {
    method: 'DELETE',
    headers: {'X-CSRFToken': csrftoken},
    mode: 'same-origin'
  })
  .then(response => {
    if (response.status === 204) {
      showMessage( successMsgTitle, successMsgBody);
      searchSchedule(getDateFromDatePickerValue($datepicker.value(), localeGijGoComponent));
    }
    else {
      throw response.error;
    }
  })
  .catch((error) => {
    console.error('Error:', error);
  });
}

// ***************************
// *** AUXILIARY Functions ***
// ***************************

function searchSchedule(date) {

  const url = constructUrlLocationSchedule(dropdownLocationButton.dataset.locationid, date);

  fetch(url)
  .then(response => response.json())
  .then(data => {

      const report = document.querySelector('#locationDailyOccupancy');
      const reportContainer = document.querySelector('#locationDailyOccupancyChart');
      clearNode(reportContainer);
      const list = document.querySelector('#locationSchedule');
      clearNode(list);
      const listHeading = document.createElement('h5');
      if (data.schedule.length === 0) {
        report.classList.remove('d-flex');
        report.classList.add('d-none');

        listHeading.innerHTML = gettext('Empty Schedule');
        list.append(listHeading);
      }
      else {
        report.classList.remove('d-none');
        report.classList.add('d-flex');

        listHeading.id = 'scheduleHeading';
        listHeading.innerHTML = gettext('Schedule');
        list.append(listHeading);
        const node = document.importNode(document.querySelector('#scheduleFilterTemplate').content, true);
        list.append(node);
        document.querySelector('#scheduleFilterContainer').addEventListener('schedule_filter', (event) => handleScheduleFilterClick(event));

      }


      let booked = 0;
      let available = 0;

      data.schedule.forEach( (scheduleItem)  => {
        let element;
        if (scheduleItem.booking) {
          element = createBooking(scheduleItem.booking);
          booked++;
        }
        else if (scheduleItem.availability) {
          element = createAvailability(scheduleItem.availability);
          available++;
        }
        list.append(element);
      });

      list.style.display = 'block';

      appendDailyOccupancyChart(reportContainer, $datepicker.value(), booked, available);
  })
}

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
  const a = document.createElement('div');
  a.id = 'booking';
  a.dataset.bookingid = data.id;
  a.className = 'container p-3 my-3 border border-dark d-flex flex-row justify-content-between align-items-center bg-info';

  // create availability info container
  const aInfo = document.createElement('div');
  aInfo.id = 'bookingInfo';
  a.append(aInfo);

  // WHEN
  const whenContainer = document.createElement('div');
  whenContainer.className = 'font-weight-bold'
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

  // create CANCEL action button
  const aAction = document.createElement('div');
  aAction.id = 'bookingCancelAction';
  aAction.append(createActionButton(document, 'bookingCancelButton', data.id, 'btn btn-danger btn-sm', gettext('Cancel'), handleCancelBookingClick));
  a.append(aAction);

  return a;
}

function createAvailability(data) {
  // create availability container
  const a = document.createElement('div');
  a.id = 'availability';
  a.dataset.availabilityid = data.id;
  a.className = 'container p-3 my-3 border d-flex flex-row justify-content-between align-items-center';

  // create availability info container
  const aInfo = document.createElement('div');
  aInfo.id = 'availabilityInfo';
  a.append(aInfo);

  // WHEN
  const whenContainer = document.createElement('div');
  whenContainer.innerHTML = toFormattedTime(new Date(Date.parse(data.when)));
  aInfo.append(whenContainer);

  // WHAT
  const whatContainer = document.createElement('div');
  whatContainer.innerHTML = data.what.name;
  aInfo.append(whatContainer);

  // create CANCEL action button
  const aAction = document.createElement('div');
  aAction.id = 'availabilityCancelAction';
  aAction.append(createActionButton(document, 'availabilityCancelButton', data.id, 'btn btn-warning btn-sm', gettext('Remove'), handleCancelAvailabilityClick));
  a.append(aAction);

  return a;
}

function clearNode(node) {
  const children = Array.from(node.children);
  if (children !== undefined) { children.forEach((child) => { child.remove(); }) };
  node.innerHTML = '';
}

function toFormattedTime(datetimeObj) {
  const timeFrom = datetimeObj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true });
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

function appendDailyOccupancyChart(container, seriesLabel, booked, available) {

  let dailyOccupancyData = {
    labels: [seriesLabel],
    datasets: [{
        label: gettext('Booked'),
        backgroundColor: 'blue',
        borderColor: 'blue',
        data: [booked]
    },
    {
        label: gettext('Available'),
        backgroundColor: 'LightGrey',
        borderColor: 'LightGrey',
        data: [available]
    }]
  }

  const canvas = document.createElement('canvas');
  canvas.id = 'dailyOccupancyBarChartCanvas';
  container.append(canvas);

  const occupancyCtx = canvas.getContext('2d');
  const occupancyBarChart = new Chart(occupancyCtx, {
    type: 'horizontalBar',
    data: dailyOccupancyData,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        xAxes: [{ stacked: true }],
        yAxes: [{ stacked: true }]
      }
    }
  });
}
