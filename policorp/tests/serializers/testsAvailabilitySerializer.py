from datetime import datetime, timezone, timedelta
from django.test import TestCase
from policorp.serializers import AvailabilitySerializer, TaskSerializer, LocationSerializer
from policorp.models import User, Location, Booking, Task, Availability

class TestAvailabilitySerializer(TestCase):

    fixtures = ['testsdata.json']

    def test_availabilitySerializer_serialize(self):

        # Availability
        now = datetime.now(timezone.utc)
        tomorrow = now + timedelta(days = 1)
        loc_name = "Buenos Aires"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 30)
        a1 = Availability.objects.create_availability(tomorrow, l1, t1)

        serializer = AvailabilitySerializer(instance=a1)
        data = serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'when', 'where', 'what', 'booked']))
        self.assertEqual(data['booked'], False)
        self.assertEqual(datetime.fromisoformat(data['when']), tomorrow)
        self.assertEqual(data['what'], TaskSerializer(instance=t1).data)
        self.assertEqual(data['where'], LocationSerializer(instance=l1).data)

    def test_availabilitySerializer_deserialize(self):

        now = datetime.now(tz=timezone.utc)
        locationid = 1
        taskid = 1
        availability =  {
            'when': now.isoformat(),
            'where': locationid,
            'what': taskid
        }

        serializer = AvailabilitySerializer(data=availability)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data.get('what'), Task.objects.get(pk=taskid))
        self.assertEqual(serializer.validated_data.get('where'), Location.objects.get(pk=locationid))

    def test_availabilitySerializer_save_availability_after_deserialize(self):

        # Deserialize an availability from data
        now = datetime.now(tz=timezone.utc)
        locationid = 1
        taskid = 1
        availability =  {
            'when': now.isoformat(),
            'where': locationid,
            'what': taskid
        }
        serializer = AvailabilitySerializer(data=availability)

        # Save it
        if (serializer.is_valid()):
            availabilityObj = serializer.save()
            self.assertEqual(availabilityObj.when, now)
            self.assertEqual(availabilityObj.where, Location.objects.get(pk=locationid))
            self.assertEqual(availabilityObj.what, Task.objects.get(pk=taskid))
            self.assertEqual(availabilityObj.booked, False)
