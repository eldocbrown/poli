import { populateDropDownLocations } from './populateDropDownLocations.js'
import { populateDropDownTasks } from './populateDropDownTasks.js'
import { mySupervisedLocationsUrl, tasksUrl } from './urls.js'
import { clearNode } from './utils.js'
import { selectLocation, selectActivity } from './messages.js'

export function initialize() {
  // Location
  const locationMenuContainer = document.querySelector('#bookOnTheFlyContainer .locationSelector .dropdown .dropdown-menu')
  clearNode(locationMenuContainer)
  const dropdownLocationButton = document.querySelector('#bookOnTheFlyContainer .locationSelector .dropdown button')
  dropdownLocationButton.innerHTML = selectLocation
  delete dropdownLocationButton.dataset.locationid
  populateDropDownLocations(mySupervisedLocationsUrl, locationMenuContainer, handleLocationSelectionClick)

  // Task
  const taskMenuContainer = document.querySelector('#bookOnTheFlyContainer .taskSelector .dropdown .dropdown-menu')
  clearNode(taskMenuContainer)
  const dropdownTaskButton = document.querySelector('#bookOnTheFlyContainer .taskSelector .dropdown button')
  dropdownTaskButton.innerHTML = selectActivity
  delete dropdownTaskButton.dataset.taskid
  delete dropdownTaskButton.dataset.duration
  populateDropDownTasks(tasksUrl, taskMenuContainer, handleTaskSelectionClick)
}

function handleLocationSelectionClick(event) {
  const dropdownButton = document.querySelector('#bookOnTheFlyContainer .locationSelector .dropdown button')
  dropdownButton.innerHTML = event.currentTarget.innerHTML
  dropdownButton.dataset.locationid = event.currentTarget.dataset.locationid
}

function handleTaskSelectionClick(event) {
  const dropdownButton = document.querySelector('#bookOnTheFlyContainer .taskSelector .dropdown button')
  dropdownButton.innerHTML = event.currentTarget.innerHTML
  dropdownButton.dataset.taskid = event.currentTarget.dataset.taskid
  dropdownButton.dataset.duration = event.currentTarget.dataset.duration
}
