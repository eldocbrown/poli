import { getDateFromDatePickerValue } from '../../static/policorp/gijgoComponentUtils'

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
