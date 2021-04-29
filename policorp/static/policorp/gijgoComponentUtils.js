/**
 * Generates a Date from a GijGo DatePicker component's string value
 * @param {string} strValue A 10 character string that represents a date (with no time)
 * @return {Date} Returns a new Date object with the local time zone
 */
export function getDateFromDatePickerValue(strValue, locale = null) {

  if (strValue.length < 10) { throw 'Invalid date. Date string should have at least 10 characters' }

  const spanishLocale = 'es-es'

  const year = strValue.substring(6,10)
  const month = locale === spanishLocale ? parseInt(strValue.substring(3,5)) - 1 : parseInt(strValue.substring(0,2)) - 1
  const day = locale === spanishLocale ? strValue.substring(0,2) : strValue.substring(3,5)

  return new Date(year, month, day)
}

export function getDateTimeFromDatePickerValue(strValue, locale = null) {
  if (strValue.length < 16) { throw 'Invalid date. Date and Time string should have at least 10 characters' }

  const date = getDateFromDatePickerValue(strValue, locale)

  const hours = strValue.substring(11,13)
  date.setHours(hours)

  const minutes = strValue.substring(14,16)
  date.setMinutes(minutes)

  return date
}
