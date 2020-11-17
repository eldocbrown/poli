from django.test import TestCase
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Availability

# Create your tests here.
class TestAvailability(TestCase):

    def test_get_availability_all(self):
        """ Given 1 availability
            When requesting all availabilities
            Then 1 availability should be returned """
        a1 = Availability.objects.create_availability(datetime.now(timezone.utc))
        self.assertEqual(len(Availability.objects.get_all()), 1)

    def test_get_availability_all_ordered_by_date_ascendant(self):
        """ Given 3 availabilities
            When requesting all availabilities
            Then 3 availabilities should be returned in descendant order by schedule date """
        now = datetime.now(timezone.utc)
        a3 = Availability.objects.create_availability(now + timedelta(days = 3))
        a1 = Availability.objects.create_availability(now + timedelta(days = 1))
        a2 = Availability.objects.create_availability(now + timedelta(days = 2))
        self.assertEqual(len(Availability.objects.get_all()), 3)
        self.assertEqual(Availability.objects.get_all()[0], a1)
        self.assertEqual(Availability.objects.get_all()[1], a2)
        self.assertEqual(Availability.objects.get_all()[2], a3)

if __name__ == "__main__":
    unittest.main()
