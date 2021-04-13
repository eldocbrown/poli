import { createAvailabilitiesJsonData } from '../../static/policorp/availabilities.js'

const encode = (myDateTime) => {
  return myDateTime.toISOString().replace("Z", "+00:00")
}

describe("createAvailabilitiesJsonData", function() {

  it("returns one availability as json, without until time parameter", () => {
    const locationid = '1'
    const taskid = '1'
    const taskduration = '120'
    const when = new Date()
    const untilTime = null

    const expectedJSON = [
      {
        "locationid": locationid,
        "taskid": taskid,
        "when": encode(when)
      }
    ]

    expect(createAvailabilitiesJsonData(locationid, taskid, taskduration, when, untilTime, encode)).toEqual(expectedJSON)
  })

  it("returns one availability, with until parameter not late enough to add a second one", () => {
    const locationid = '1'
    const taskid = '1'
    const taskduration = '120'
    const when = new Date()
    const untilTime = new Date(when.getTime() + taskduration*60000).toLocaleTimeString().substring(0,5)

    const expectedJSON = [
      {
        "locationid": locationid,
        "taskid": taskid,
        "when": encode(when)
      }
    ]

    expect(createAvailabilitiesJsonData(locationid, taskid, taskduration, when, untilTime, encode)).toEqual(expectedJSON)
  })

  it("returns one availability, with until parameter not late enough to add a second one - #2", () => {
    const locationid = '1'
    const taskid = '1'
    const taskduration = '120'
    const when = new Date()
    const untilTime = new Date(when.getTime() + 1.5*taskduration*60000).toLocaleTimeString().substring(0,5)

    const expectedJSON = [
      {
        "locationid": locationid,
        "taskid": taskid,
        "when": encode(when)
      }
    ]

    expect(createAvailabilitiesJsonData(locationid, taskid, taskduration, when, untilTime, encode)).toEqual(expectedJSON)
  })

  it("returns two availabilities, with until parameter setting to fit two task durations", () => {
    const locationid = '1'
    const taskid = '1'
    const taskduration = '120'
    const when = new Date()
    const untilTime = new Date(when.getTime() + 2*taskduration*60000).toLocaleTimeString().substring(0,5)

    const expectedJSON = [
      {
        "locationid": locationid,
        "taskid": taskid,
        "when": encode(when)
      },
      {
        "locationid": locationid,
        "taskid": taskid,
        "when": encode(new Date(when.getTime() + taskduration*60000))
      }
    ]

    expect(createAvailabilitiesJsonData(locationid, taskid, taskduration, when, untilTime, encode)).toEqual(expectedJSON)
  })

  it("throws exception, with until parameter setting minor to when parameter", () => {
    const locationid = '1'
    const taskid = '1'
    const taskduration = '120'
    const when = new Date()
    const untilTime = new Date(when.getTime() - taskduration*60000).toLocaleTimeString().substring(0,5)

    expect(() => createAvailabilitiesJsonData(locationid, taskid, taskduration, when, untilTime, encode)).toThrow('Invalid time settings')

  })
})
