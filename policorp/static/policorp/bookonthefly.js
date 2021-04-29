import { populateDropDownLocations } from './populateDropDownLocations.js'
import { populateDropDownTasks } from './populateDropDownTasks.js'
import { mySupervisedLocationsUrl, tasksUrl, bookOnTheFlyUrl } from './urls.js'
import { clearNode } from './utils.js'
import { showMessage, selectLocation, selectActivity, invalidDateMsg, formNotValid, bookingPostSuccessMsg } from './messages.js'
import { encodeDateTime } from './dateTimeUtils.js'
import { getDateTimeFromDatePickerValue } from './gijgoComponentUtils.js'

document.addEventListener('DOMContentLoaded', () => {

  document.querySelector('#bookOnTheFlyContainer .buttonContainer button').addEventListener('click', () => handleBookButtonClick())

})

let datetimepicker = undefined

export function initialize() {
  // Location dropdown
  const locationMenuContainer = document.querySelector('#bookOnTheFlyContainer .locationSelector .dropdown .dropdown-menu')
  clearNode(locationMenuContainer)
  const dropdownLocationButton = document.querySelector('#bookOnTheFlyContainer .locationSelector .dropdown button')
  dropdownLocationButton.innerHTML = selectLocation
  delete dropdownLocationButton.dataset.locationid
  populateDropDownLocations(mySupervisedLocationsUrl, locationMenuContainer, handleLocationSelectionClick)

  // Task dropdown
  const taskMenuContainer = document.querySelector('#bookOnTheFlyContainer .taskSelector .dropdown .dropdown-menu')
  clearNode(taskMenuContainer)
  const dropdownTaskButton = document.querySelector('#bookOnTheFlyContainer .taskSelector .dropdown button')
  dropdownTaskButton.innerHTML = selectActivity
  delete dropdownTaskButton.dataset.taskid
  delete dropdownTaskButton.dataset.duration
  populateDropDownTasks(tasksUrl, taskMenuContainer, handleTaskSelectionClick)

  // Date Picker
  const date = new Date()
  datetimepicker = $('#bookOnTheFlyContainer .dateTimePickerContainer input[name="datetime"]').datetimepicker({
    footer: true,
    modal: true,
    width: 200,
    uiLibrary: 'bootstrap4',
    locale: localeGijGoComponent,
    format: formatGijGoDateComponent + ' HH:MM'
  })
  datetimepicker.value(date.toLocaleDateString(localeGijGoComponent, optionsGijGoDateComponent) + ' ' + date.toLocaleTimeString(localeGijGoComponent, { hour: '2-digit', minute: '2-digit' }))

  // Note
  document.querySelector('#bookOnTheFlyContainer .noteContainer textarea.note').value = ''

}

function handleLocationSelectionClick(event) {
  const dropdownButton = document.querySelector('#bookOnTheFlyContainer .locationSelector .dropdown button')
  dropdownButton.innerHTML = event.currentTarget.innerHTML
  dropdownButton.dataset.locationid = event.currentTarget.dataset.locationid
  evaluateBookButtonState()
}

function handleTaskSelectionClick(event) {
  const dropdownButton = document.querySelector('#bookOnTheFlyContainer .taskSelector .dropdown button')
  dropdownButton.innerHTML = event.currentTarget.innerHTML
  dropdownButton.dataset.taskid = event.currentTarget.dataset.taskid
  dropdownButton.dataset.duration = event.currentTarget.dataset.duration
  evaluateBookButtonState()
}

function handleBookButtonClick() {

  try {
    if (formIsValid()) { // Validate form
      doBook(contentJSONGenerator) // Post the booking
      .then(
        (booking) => { // Resolved
          showMessage( gettext('Success'), bookingPostSuccessMsg )
          initialize()
        }
        , (error) => showMessage('Error', error)) // Rejected
    }
    else {
      showMessage('Error', formNotValid) // Invalid Form
    }
  }
  catch(err) {
    showMessage('Error', err) // Something didn't work as expected
  }

}

function formIsValid() {
  const dateTimeValue = document.querySelector('#bookOnTheFlyContainer .dateTimePickerContainer input[name="datetime"]').value
  if (dateTimeValue === undefined) {
    throw invalidDateMsg
  }
  else if (dateTimeValue.length < 16 ){
    throw invalidDateMsg
  }
  return true
}

function doBook(contentJSONGenerator) {
  const contentJSON = contentJSONGenerator()
  return fetch(bookOnTheFlyUrl, {
    method: 'POST',
    headers: { 'X-CSRFToken': csrftoken, 'Content-Type': 'application/json' },
    mode: 'same-origin',
    body: JSON.stringify(contentJSON)
  })
  .then(response => {
    if (response.status === 204) {
      return Promise.resolve(contentJSON)
    }
    else {
        throw `Response status code: ${response.status}`
    }
  })
  .catch((error) => {
    return Promise.reject(error)
  })
}

function contentJSONGenerator() {

  const noteTxtArea = document.querySelector('#bookOnTheFlyContainer .noteContainer textarea')
  const whereButton = document.querySelector('#bookOnTheFlyContainer .locationSelector .dropdown button')
  const whatButton = document.querySelector('#bookOnTheFlyContainer .taskSelector .dropdown button')

  const json = {
    "availability": {
      "when": encodeDateTime(getDateTimeFromDatePickerValue(datetimepicker.value(), localeGijGoComponent)),
      "where": whereButton.dataset.locationid,
      "what": whatButton.dataset.taskid
    },
    "note": noteTxtArea.value,
    "user": username
  }

  return json
}

function evaluateBookButtonState() {
  const location = document.querySelector('#bookOnTheFlyContainer .locationSelector .dropdown button')
  const task = document.querySelector('#bookOnTheFlyContainer .taskSelector .dropdown button')
  const button = document.querySelector('#bookOnTheFlyContainer .buttonContainer button')

  if ((!isNaN(location.dataset.locationid)) && (!isNaN(task.dataset.taskid))) {
    button.disabled = false;
    button.style.cursor = 'pointer';
  }
}
