from django.test import TestCase
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Availability, Location

# Create your tests here.
class TestAvailability(TestCase):

    def test_get_availability_all(self):
        """ GIVEN 1 availability; WHEN requesting all availabilities; THEN 1 availability should be returned """

        loc_name = "Buenos Aires"
        l1 = Location.objects.create_location(loc_name)
        a1 = Availability.objects.create_availability(datetime.now(timezone.utc), l1)
        self.assertEqual(len(Availability.objects.get_all()), 1)

    def test_get_availability_all_ordered_by_date_ascendant(self):
        """ GIVEN 3 availabilities; WHEN requesting all availabilities; THEN 3 availabilities should be returned in descendant order by schedule date """

        loc_name = "Buenos Aires"
        l1 = Location.objects.create_location(loc_name)
        now = datetime.now(timezone.utc)
        a3 = Availability.objects.create_availability(now + timedelta(days = 3), l1)
        a1 = Availability.objects.create_availability(now + timedelta(days = 1), l1)
        a2 = Availability.objects.create_availability(now + timedelta(days = 2), l1)
        self.assertEqual(len(Availability.objects.get_all()), 3)
        self.assertEqual(Availability.objects.get_all()[0], a1)
        self.assertEqual(Availability.objects.get_all()[1], a2)
        self.assertEqual(Availability.objects.get_all()[2], a3)

    def test_get_availability_all_with_location(self):
        """GIVEN 1 availability at Buenos Aires, tomorrow; WHEN requesting all availabilities; THEN 1 availability should be returned at Buenos Aires, tomorrow"""

        now = datetime.now(timezone.utc)
        tomorrow = now + timedelta(days = 1)
        loc_name = "Buenos Aires"
        l1 = Location.objects.create_location(loc_name)
        a1 = Availability.objects.create_availability(tomorrow, l1)
        self.assertEqual(len(Availability.objects.get_all()), 1)
        availability = Availability.objects.get_all()[0]
        self.assertEqual(availability.WHEN, tomorrow)
        self.assertEqual(availability.where.name, loc_name)

class TestLocation(TestCase):

    def test_get_location_all(self):
        """ GIVEN 1 location; WHEN requesting all locations; THEN 1 location should be returned """

        loc_name = "Buenos Aires"
        l = Location.objects.create_location(loc_name)
        self.assertEqual(len(Location.objects.get_all()), 1)

    def test_get_location_all_gets_name(self):
        """ GIVEN 1 location with name "Buenos Aires"; WHEN requesting all locations; THEN 1 location should be returned with name "Buenos Aires" """

        loc_name = "Buenos Aires"
        l = Location.objects.create_location(loc_name)
        self.assertEqual(len(Location.objects.get_all()), 1)
        self.assertEqual(Location.objects.get_all()[0].name, loc_name)

if __name__ == "__main__":
    unittest.main()
