export const emptyScheduleHeading = gettext('Empty Schedule')
export const availabilityCancelledMsgTitle = gettext('Availability removed')
export const availabilityCancelledMsgBody = gettext('You have successfully removed the availability')
export const noteLabel = gettext('Note')
export const selectLocation = gettext('Select location')
export const selectActivity = gettext('Select activity')
export const invalidDateMsg = gettext('Invalid date')
export const formNotValid = gettext('Form not valid')
export const bookingPostSuccessMsg = gettext('You have successfully created the booking.')
export const bookedTxt = gettext('Booked')
export const availableTxt = gettext('Available')

export function showMessage(title, message) {
  document.querySelector('#messageModalLabel').innerHTML = title;
  document.querySelector('#messageModalBody').innerHTML = message;
  $("#messageModal").modal('show');
}
