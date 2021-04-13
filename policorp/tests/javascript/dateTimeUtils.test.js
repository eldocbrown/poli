import { addMinutes } from '../../static/policorp/dateTimeUtils.js'

describe("addMinutes", () => {

  it("when 0 minutes are added, then it returns the same date", () => {
    const now = new Date()

    expect(addMinutes(now, 0)).toEqual(now)
  })

  it("when 2 minutes are added, then it returns the same date plus two minutes ahead", () => {
    const now = new Date()
    const minutesToAdd = 2

    expect(addMinutes(now, minutesToAdd)).toEqual(new Date(now.getTime() + minutesToAdd*60000))
  })

  it("when 10 negative minutes are added, then it returns the same date minus ten minutes earlier", () => {
    const now = new Date()
    const minutesToAdd = -10

    expect(addMinutes(now, minutesToAdd)).toEqual(new Date(now.getTime() + minutesToAdd*60000))
  })

})
