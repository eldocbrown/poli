import { addMinutes } from './dateTimeUtils.js'

export function createAvailabilitiesJsonData(locationid, taskid, taskduration, when, untilTime, encoder) {

  let json = [{
              "locationid": locationid,
              "taskid": taskid,
              "when": encoder(when)
          }];

  if (untilTime !== null) {
    let until = new Date(when);
    until.setHours(untilTime.substring(0, 2));
    until.setMinutes(untilTime.substring(3, 5));

    if (until < when) throw "Invalid time settings";

    let newWhenBegin = addMinutes(when, taskduration);
    let newWhenEnd = addMinutes(newWhenBegin, taskduration);

    while (newWhenEnd <= until) {
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
