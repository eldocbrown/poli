document.addEventListener('DOMContentLoaded', () => {

  loadFilters();
  document.querySelector('#locationScheduleContainer').style.display = 'block';
  document.querySelector('#locationConfigurationContainer').style.display = 'none';
  document.querySelector('#location-schedule-link').addEventListener('click', () => handleLocationScheduleLinkClick());
  document.querySelector('#location-config-link').addEventListener('click', () => handleLocationConfigurationLinkClick());
  document.querySelector('#lookupBookingsButton').addEventListener('click', (event) => handleSearchClick(event));

});

// ********************************
// *** EVENT HANDLERS Functions ***
// ********************************

function handleLocationScheduleLinkClick() {
  document.querySelector('#locationScheduleContainer').style.display = 'block';
  document.querySelector('#locationConfigurationContainer').style.display = 'none';
}

function handleLocationConfigurationLinkClick() {
  document.querySelector('#locationScheduleContainer').style.display = 'none';
  document.querySelector('#locationConfigurationContainer').style.display = 'block';
}

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

/*
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
          const fromDatetime = new Date(Date.parse(data.availability.when));
          const fromDatetimeStr = toFormattedDateTime(fromDatetime, data.availability.what.duration);

          showMessage('Booking confirmed', `You have successfully booked the task ${task} on ${fromDatetimeStr}`);
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
        const datetime = toFormattedDateTime(new Date(Date.parse(data.availability.when)), data.availability.what.duration);
        showMessage('Booking cancelled', `You have successfully cancelled the task ${task} on ${datetime}`);
      } else {
        console.error(data);
      }

      loadMySchedule()
  });
}

function handleDownloadCalClick(event) {
  const button = event.currentTarget;
  const dateStart = new Date(Date.parse(button.dataset.when));
  const dateEnd = new Date(dateStart.getTime() + button.dataset.duration*60000);
  downloadIcsFile(dateStart, dateEnd, button.dataset.what, button.dataset.what, button.dataset.where);
}
*/
//function handleLocationLinkClick(event) {
  //const link = event.currentTarget;
  //const query = event.currentTarget.dataset.where.replace(/  */g, '+');
  //const url = `https://www.google.com/maps/search/?api=1&query=${query}`;
  //window.open(url);
//}

// ***************************
// *** AUXILIARY Functions ***
// ***************************

function loadFilters() {

  populateLocations(document.querySelector('#taskDropdownMenu'));

  document.querySelector('#locationSelector').style.display = 'block';
  document.querySelector('#locationSchedule').style.display = 'none';

}

/*
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
*/
function populateLocations(dropDown) {
  fetch(`/policorp/mysupervisedlocations/`)
  .then(response => response.json())
  .then(data => {
      data.forEach( function(location) {
        const option = document.createElement('a');
        option.classList.add('dropdown-item');
        option.id = 'locationOption';
        option.dataset.locationid = location.id;
        option.innerHTML = location.name;
        option.addEventListener('click', (event) => handleLocationSelectionClick(event));

        dropDown.append(option);
      });
  })
}

function constructUrlLocationSchedule(locationid, date) {
  return `/policorp/locationschedule/${locationid}/${date.getFullYear()}${date.getMonth() + 1}${date.getDate()}`
}
/*
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
  whenContainer.innerHTML = toFormattedDateTime(new Date(Date.parse(data.when)), data.what.duration);
  aInfo.append(whenContainer);

  // WHERE
  const whereContainer = document.createElement('div');
  whereContainer.innerHTML = data.where.name;
  const link = createLocationLink(data.where.name);
  whereContainer.append(link);
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
*/
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
/*
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
*/
  return a;
}
/*
function createLocationLink(location) {
  const link = document.createElement('img');
  link.id = 'downloadCalIcon';
  link.src = 'static/policon/image/geo-alt-fill.svg';
  link.title = 'Open in Google Maps';
  link.dataset.where = location;
  link.addEventListener('click', (event) => handleLocationLinkClick(event));
  return link;
}
*/
function clearNode(node) {
  var children = Array.from(node.children);
  if (children !== undefined) { children.forEach((child) => { child.remove(); }) };
  node.innerHTML = '';
}

function toFormattedTime(datetimeObj) {
  timeFrom = datetimeObj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true });
  return (timeFrom);
}
/*
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

function showMessage(title, message) {
  document.querySelector('#messageModalLabel').innerHTML = title;
  document.querySelector('#messageModalBody').innerHTML = message;
  $("#messageModal").modal('show');
}

function downloadIcsFile(dateStart, dateEnd, summary, description, location) {

  this._isofix2 = function(d) {
      const dateStr = d.toISOString();

      let fixedDateStr = dateStr.replace(/\-/g, '');
      fixedDateStr = fixedDateStr.replace(/\:/g, '');
      fixedDateStr = fixedDateStr.replace(/\.[0-9][0-9][0-9]/g, '');
		  return fixedDateStr;
	}

  const now = new Date();

  var ics_lines = [
    "BEGIN:VCALENDAR",
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH",
    "PRODID:-//Poli Cal//EN",
    "VERSION:2.0",
    "BEGIN:VEVENT",
    "UID:event-" + now.getTime() + "@poli.com",
    "DTSTAMP:"+ this._isofix2(now),
    "DTSTART:" + this._isofix2(dateStart),
    "DTEND:" + this._isofix2(dateEnd),
    "SUMMARY:" + summary,
    "LOCATION:" + location,
    "DESCRIPTION:" + description,
    "END:VEVENT",
    "END:VCALENDAR"
  ];

  var dlurl = 'data:text/calendar;base64,'+btoa(ics_lines.join('\r\n'));

  var save = document.createElement('a');
  save.href = dlurl;
  save.target = '_blank';
  save.download = 'calendar.ics';
  var evt = new MouseEvent('click', {
	   'view': window,
     'bubbles': true,
     'cancelable': false
  });
  save.dispatchEvent(evt);

  (window.URL || window.webkitURL).revokeObjectURL(save.href);
}
*/
