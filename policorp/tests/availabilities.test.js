import { createAvailabilitiesJsonData } from '../static/policorp/availabilities.js'

describe("createAvailabilitiesJsonData", function() {
  it("returns one availability as json, without until time parameter", function() {
    const locationid = '1'
    const taskid = '1'
    const taskduration = '120'
    const when = new Date()
    const untilTime = null

    const encoder = (myDateTime) => {
      return myDateTime.toISOString().replace("Z", "+00:00")
    }

    const encodedWhen = encoder(when)

    const expectedJSON = [
      {
        "locationid": locationid,
        "taskid": taskid,
        "when": encodedWhen
      }
    ]

    expect(createAvailabilitiesJsonData(locationid, taskid, taskduration, when, untilTime, encoder)).toEqual(expectedJSON)
  })
})
