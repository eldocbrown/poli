import { addMinutes } from './dateTimeUtils.js'

export function createAvailabilitiesJsonData(locationid, taskid, taskduration, when, untilDateTime, encoder) {

  let json = [{
              "locationid": locationid,
              "taskid": taskid,
              "when": encoder(when)
          }];

  if (untilDateTime !== null) {

    if (untilDateTime < when) throw "Invalid time settings";

    let newWhenBegin = addMinutes(when, taskduration);
    let newWhenEnd = addMinutes(newWhenBegin, taskduration);

    while (newWhenEnd <= untilDateTime) {
      json.push({
                "locationid": locationid,
                "taskid": taskid,
                "when": encoder(newWhenBegin)
                });

      newWhenBegin = addMinutes(newWhenBegin, taskduration);
      newWhenEnd = addMinutes(newWhenBegin, taskduration);
    }
  }

  return json;
}

export function appendNewAvailabilityDatesToJsonData(initialAvailabilityJson, days, fromDate, untilDate, dateTimeEncoder, dateTimeDecoder) {

  let json = JSON.parse(JSON.stringify(initialAvailabilityJson));
  let currentDate = new Date(fromDate);
  currentDate.setDate(currentDate.getDate() + 1);
  currentDate.setHours(0,0,0,0)
  while (currentDate <= untilDate) {
    if (days[currentDate.getDay()] === true) {
      initialAvailabilityJson.forEach(a => {
        const newWhen = dateTimeDecoder(a["when"]);
        newWhen.setDate(currentDate.getDate());
        newWhen.setMonth(currentDate.getMonth());
        newWhen.setFullYear(currentDate.getFullYear());
        json.push({
                  "locationid": a["locationid"],
                  "taskid": a["taskid"],
                  "when": dateTimeEncoder(newWhen)
                  });
      });
    }
    currentDate.setDate(currentDate.getDate() + 1);
  }

  return json;
}
