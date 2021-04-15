import { createAvailabilitiesJsonData, appendNewAvailabilityDatesToJsonData } from '../../static/policorp/availabilities.js'

const encode = (myDateTime) => {
  return myDateTime.toISOString().replace("Z", "+00:00")
}

const decode = (datetimestring) => {
  return new Date(datetimestring.replace("+00:00", "Z"));
}

function newDatePlusDays(date, days) {
  const newDate = new Date(date)
  newDate.setDate(newDate.getDate() + days)
  return newDate
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
    const untilTime = new Date(when.getTime() + taskduration*60000).toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit' }).substring(0,5)

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
    const untilTime = new Date(when.getTime() + 1.5*taskduration*60000).toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit' }).substring(0,5)

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
    const untilTime = new Date(when.getTime() + 2*taskduration*60000).toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit' }).substring(0,5)

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
    const untilTime = new Date(when.getTime() - taskduration*60000).toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit' }).substring(0,5)

    expect(() => createAvailabilitiesJsonData(locationid, taskid, taskduration, when, untilTime, encode)).toThrow('Invalid time settings')

  })
})


describe("appendNewAvailabilityDatesToJsonData", function() {

  it("returns the same json when all days are false", () => {

    const when = new Date()

    const initialJSON = [
      {
        "locationid": '1',
        "taskid": '1',
        "when": encode(when)
      }
    ]

    let days = [false, false, false, false, false, false, false];
    let untilDate = new Date(when.getFullYear(), when.getMonth(), when.getDate(), 0,0,0,0);

    expect(appendNewAvailabilityDatesToJsonData(initialJSON, days, when, untilDate, encode, decode)).toEqual(initialJSON)

  })

  it("returns availabilities with today and tomorrow", () => {

    const when = new Date()

    const initialJSON = [
      {
        "locationid": '1',
        "taskid": '1',
        "when": encode(when)
      }
    ]

    const days = [true, true, true, true, true, true, true]
    let untilDate = new Date()
    untilDate.setDate(when.getDate() + 1)
    untilDate.setHours(0,0,0,0)

    const expectedJSON = [
      {
        "locationid": '1',
        "taskid": '1',
        "when": encode(when)
      },
      {
        "locationid": '1',
        "taskid": '1',
        "when": encode(newDatePlusDays(when,1))
      }
    ]

    expect(appendNewAvailabilityDatesToJsonData(initialJSON, days, when, untilDate, encode, decode)).toEqual(expectedJSON)

  })

  it("returns availabilities with today and the day after tomorrow", () => {

    const when = new Date()
    const taskduration = 120

    const initialJSON = [
      {
        "locationid": '1',
        "taskid": '1',
        "when": encode(when)
      },
      {
        "locationid": '1',
        "taskid": '1',
        "when": encode(new Date(when.getTime() + taskduration*60000))
      }
    ]

    const days = [true, true, true, true, true, true, true]
    days[when.getDay() + 1] = false
    const untilDate = newDatePlusDays(when,2)
    untilDate.setHours(0,0,0,0)

    const expectedJSON = [
      {
        "locationid": '1',
        "taskid": '1',
        "when": encode(when)
      },
      {
        "locationid": '1',
        "taskid": '1',
        "when": encode(new Date(when.getTime() + taskduration*60000))
      },
      {
        "locationid": '1',
        "taskid": '1',
        "when": encode(newDatePlusDays(when,2))
      },
      {
        "locationid": '1',
        "taskid": '1',
        "when": encode(new Date(newDatePlusDays(when,2).getTime() + taskduration*60000))
      }
    ]

    expect(appendNewAvailabilityDatesToJsonData(initialJSON, days, when, untilDate, encode, decode)).toEqual(expectedJSON)

  })

  it("issue poli#2", () => {

    const MARCH = 2

    const when = new Date(2021, MARCH, 1, 9, 0, 0, 0)
    const taskduration = 45

    const initialJSON = [
      {
        "locationid": '1',
        "taskid": '1',
        "when": encode(when)
      }
    ]

    const days = [false, true, true, true, true, true, false]

    const untilDate = newDatePlusDays(when, 4)
    untilDate.setHours(0,0,0,0)

    const expectedJSON = [
      {
        "locationid": '1',
        "taskid": '1',
        "when": encode(when)
      },
      {
        "locationid": '1',
        "taskid": '1',
        "when": encode(newDatePlusDays(when, 1))
      },
      {
        "locationid": '1',
        "taskid": '1',
        "when": encode(newDatePlusDays(when, 2))
      },
      {
        "locationid": '1',
        "taskid": '1',
        "when": encode(newDatePlusDays(when, 3))
      },
      {
        "locationid": '1',
        "taskid": '1',
        "when": encode(newDatePlusDays(when, 4))
      }
    ]

    expect(appendNewAvailabilityDatesToJsonData(initialJSON, days, when, untilDate, encode, decode)).toEqual(expectedJSON)

  })

  it("issue poli#2 - end of month", () => {

    const MARCH = 2
    const APRIL = 3

    const when = new Date(2021, MARCH, 31, 9, 0, 0, 0)
    const taskduration = 45

    const initialJSON = [
      {
        "locationid": '1',
        "taskid": '1',
        "when": encode(when)
      }
    ]

    const days = [true, true, true, true, true, true, true]

    const untilDate = newDatePlusDays(when, 4)
    untilDate.setHours(0,0,0,0)

    const expectedJSON = [
      {
        "locationid": '1',
        "taskid": '1',
        "when": encode(when)
      },
      {
        "locationid": '1',
        "taskid": '1',
        "when": encode(newDatePlusDays(when, 1))
      },
      {
        "locationid": '1',
        "taskid": '1',
        "when": encode(newDatePlusDays(when, 2))
      },
      {
        "locationid": '1',
        "taskid": '1',
        "when": encode(newDatePlusDays(when, 3))
      },
      {
        "locationid": '1',
        "taskid": '1',
        "when": encode(newDatePlusDays(when, 4))
      }
    ]

    expect(appendNewAvailabilityDatesToJsonData(initialJSON, days, when, untilDate, encode, decode)).toEqual(expectedJSON)

  })

})
