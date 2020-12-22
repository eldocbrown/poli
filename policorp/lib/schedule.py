from policorp.models import Availability, Booking

class Schedule:

    def __init__(self, date, location, availabilities, bookings):
        self.date = date
        self.location = location
        self.availabilities = availabilities
        self.bookings = bookings

    def toSortedScheduleArray(self):
        arr1 = sorted(self.availabilities, key=lambda a: a.when)
        arr2 = sorted(self.bookings, key=lambda b: b.availability.when)
        n1 = len(arr1)
        n2 = len(arr2)
        arr3 = [None]*(n1 + n2)
        i = 0
        j = 0
        k = 0

        # Traverse both array
        while i < n1 and j < n2:
            # Check if current element of first array is smaller than current element of
            # second array. If yes, store first array element and increment first array
            # index. Otherwise do same with second array
            if arr1[i].when < arr2[j].availability.when:
                arr3[k] = arr1[i]
                k = k + 1
                i = i + 1
            else:
                arr3[k] = arr2[j]
                k = k + 1
                j = j + 1

        # Store remaining elements of first array
        while i < n1:
            arr3[k] = arr1[i]
            k = k + 1
            i = i + 1

        # Store remaining elements of second array
        while j < n2:
            arr3[k] = arr2[j]
            k = k + 1
            j = j + 1

        return arr3

    def json(self):

        def json_sch(x):
            json = {}
            if isinstance(x, Booking):
                json = {'booking': x.json()}
            elif isinstance(x, Availability):
                json = {'availability': x.json()}
            return json

        return  {
                    'date': self.date.isoformat(),
                    'location': self.location.json(),
                    'schedule': [ json_sch(s) for s in self.toSortedScheduleArray()]
                }
