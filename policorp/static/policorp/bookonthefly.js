import { populateDropDownLocations } from './populateDropDownLocations.js'
import { populateDropDownTasks } from './populateDropDownTasks.js'
import { mySupervisedLocationsUrl, tasksUrl } from './urls.js'
import { clearNode } from './utils.js'
import { showMessage, selectLocation, selectActivity, invalidDateMsg, formNotValid } from './messages.js'

document.addEventListener('DOMContentLoaded', () => {

  document.querySelector('#bookOnTheFlyContainer .buttonContainer button').addEventListener('click', () => handleBookButtonClick())

})

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
  const datetimepicker = $('#bookOnTheFlyContainer .dateTimePickerContainer input[name="datetime"]').datetimepicker({
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
    if (formIsValid()) {
      doBook()
      initialize()
    }
    else {
      console.log(formNotValid)
    }
  }
  catch(err) {
    showMessage('Error', err)
  }

}

function formIsValid() {
  if (document.querySelector('#bookOnTheFlyContainer .dateTimePickerContainer input[name="datetime"]').value !== "") {
    return true
  }
  else {
    throw invalidDateMsg
  }
}

function doBook() {
  // TODO
  console.log('booked')
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
