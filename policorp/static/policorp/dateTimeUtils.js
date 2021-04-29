export function addMinutes(dt, minutes) {
    return new Date(dt.getTime() + minutes*60000);
}

export function toFormattedDuration(duration) {
  if (duration < 60) {
    return `${duration} min`;
  } else {
    const hours = Math.floor(duration / 60);
    const minutes = duration % 60;
    if (minutes !== 0) { return `${hours} hs ${minutes} min`; }
    else { return `${hours} hs`; }
  }
}

export function encodeDateTime(datetime) {
  return datetime.toISOString().replace("Z", "+00:00");
}

export function decodeDateTime(datetimestring) {
  return new Date(datetimestring.replace("+00:00", "Z"));
}
