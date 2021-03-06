import { getDateFromDatePickerValue, getDateTimeFromDatePickerValue } from '../../static/policorp/gijgoComponentUtils'

describe('getDateFromDatePickerValue', () => {

  it('gets new Date with en-us locale by default', () => {
    const value = '04/06/1982'

    const date = getDateFromDatePickerValue(value)

    expect(date.getFullYear()).toBe(1982)
    expect(date.getMonth()).toBe(3) // April
    expect(date.getDate()).toBe(6)
  })

  it('gets new Date with en-us', () => {
    const value = '04/06/1982'

    const date = getDateFromDatePickerValue(value)

    expect(date.getFullYear()).toBe(1982)
    expect(date.getMonth()).toBe(3) // April
    expect(date.getDate()).toBe(6)
  })

  it('gets new Date with es-es', () => {
    const value = '06/04/1982'
    const locale = 'es-es'

    const date = getDateFromDatePickerValue(value, locale)

    expect(date.getFullYear()).toBe(1982)
    expect(date.getMonth()).toBe(3) // April
    expect(date.getDate()).toBe(6)
  })

  it('throws and error when strValue has less than 10 characters', () => {

    const value = '06/4/1982'
    const locale = 'es-es'

    expect(() => getDateFromDatePickerValue(value, locale)).toThrow()

  })

})

describe('getDateTimeFromDatePickerValue', () => {

  it('gets new Date with en-us locale by default', () => {
    const value = '04/06/1982 21:15'
    const offset = new Date().getTimezoneOffset()

    const date = getDateTimeFromDatePickerValue(value)

    expect(date.getFullYear()).toBe(1982)
    expect(date.getMonth()).toBe(3) // April
    expect(date.getDate()).toBe(6)

    expect(date.getHours()).toBe(21)
    expect(date.getMinutes()).toBe(15)
    expect(date.getSeconds()).toBe(0)
    expect(date.getMilliseconds()).toBe(0)
    expect(date.getTimezoneOffset()).toBe(new Date().getTimezoneOffset()) // Local Time

  })

  it('throws and error when strValue has less than 16 characters', () => {

    const value = '06/4/1982'
    const locale = 'es-es'

    expect(() => getDateTimeFromDatePickerValue(value, locale)).toThrow()

  })

})
