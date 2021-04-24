from django.test import TestCase
from datetime import datetime, timedelta, time
from django.utils import timezone
from policorp.models import Availability, Booking, Location, Task
from policorp.tests import aux
import json

class TestAvailability(TestCase):

    def test_get_availability_all(self):
        """ GIVEN 1 availability; WHEN requesting all availabilities; THEN 1 availability should be returned """

        loc_name = "Buenos Aires"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 30)
        a1 = Availability.objects.create_availability(datetime.now(timezone.utc), l1, t1)
        self.assertEqual(len(Availability.objects.get_all()), 1)

    def test_get_availability_all_ordered_by_date_ascendant_1(self):
        """ GIVEN 3 availabilities; WHEN requesting all availabilities; THEN 3 availabilities should be returned in ascendant order by schedule date """

        loc_name = "Buenos Aires"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 30)
        now = datetime.now(timezone.utc)
        a3 = Availability.objects.create_availability(now + timedelta(days = 3), l1, t1)
        a1 = Availability.objects.create_availability(now + timedelta(days = 1), l1, t1)
        a2 = Availability.objects.create_availability(now + timedelta(days = 2), l1, t1)
        self.assertEqual(len(Availability.objects.get_all()), 3)
        self.assertEqual(Availability.objects.get_all()[0], a1)
        self.assertEqual(Availability.objects.get_all()[1], a2)
        self.assertEqual(Availability.objects.get_all()[2], a3)

    def test_get_availability_all_ordered_by_date_ascendant_2(self):
        """ GIVEN 3 availabilities, 1 booked; WHEN requesting all availabilities; THEN 2 availabilities should be returned in ascendant order by schedule date """

        loc_name = "Buenos Aires"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 30)
        now = datetime.now(timezone.utc)
        a3 = Availability.objects.create_availability(now + timedelta(days = 3), l1, t1)
        a1 = Availability.objects.create_availability(now + timedelta(days = 1), l1, t1)
        a2 = Availability.objects.create_availability(now + timedelta(days = 2), l1, t1)
        a2.book()
        self.assertEqual(len(Availability.objects.get_all()), 2)
        self.assertIn(a1, Availability.objects.get_all())
        self.assertIn(a3, Availability.objects.get_all())
        self.assertTrue(Availability.objects.get_all()[0].when < Availability.objects.get_all()[1].when)

    def test_get_availability_all_with_location(self):
        """GIVEN 1 availability at Buenos Aires, tomorrow; WHEN requesting all availabilities; THEN 1 availability should be returned at Buenos Aires, tomorrow"""

        now = datetime.now(timezone.utc)
        tomorrow = now + timedelta(days = 1)
        loc_name = "Buenos Aires"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 30)
        a1 = Availability.objects.create_availability(tomorrow, l1, t1)
        self.assertEqual(len(Availability.objects.get_all()), 1)
        availability = Availability.objects.get_all()[0]
        self.assertEqual(availability.when, tomorrow)
        self.assertEqual(availability.where.name, loc_name)

    def test_get_availability_all_by_task(self):
        """ GIVEN 1 availability at Cordoba, tomorrow, for "Device Installation", WHEN requesting all availabilities for "Device Installation", THEN 1 availability should be returned at Cordoba, tomorrow for "Device Installation" """

        now = datetime.now(timezone.utc)
        tomorrow = now + timedelta(days = 1)
        loc_name = "Cordoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 30)
        a1 = Availability.objects.create_availability(tomorrow, l1, t1)
        self.assertEqual(len(Availability.objects.get_all_by_task(task_name)), 1)
        availability = Availability.objects.get_all_by_task(task_name)[0]
        self.assertEqual(availability.when, tomorrow)
        self.assertEqual(availability.where.name, loc_name)
        self.assertEqual(availability.what.name, task_name)

    def test_get_availability_all_by_task_ordered_by_date_ascendant_1(self):
        """ GIVEN 3 availabilities, 1 for Device Installation, 2 for Repair; WHEN requesting all availabilities for "Repair"; THEN 2 availabilities should be returned in ascendant order by schedule date for task "Repair" """

        loc_name = "Buenos Aires"
        l1 = Location.objects.create_location(loc_name)
        install = Task.objects.create_task("Device Installation", 30)
        repair = Task.objects.create_task("Repair", 30)
        now = datetime.now(timezone.utc)
        a3 = Availability.objects.create_availability(now + timedelta(days = 3), l1, install)
        a2 = Availability.objects.create_availability(now + timedelta(days = 2), l1, repair)
        a1 = Availability.objects.create_availability(now + timedelta(days = 1), l1, repair)
        self.assertEqual(len(Availability.objects.get_all_by_task(repair.name)), 2)
        self.assertIn(a1, Availability.objects.get_all_by_task(repair.name))
        self.assertIn(a2, Availability.objects.get_all_by_task(repair.name))
        self.assertTrue(Availability.objects.get_all_by_task(repair.name)[0].when < Availability.objects.get_all_by_task(repair.name)[1].when)
        self.assertEqual(Availability.objects.get_all_by_task(repair.name)[0].what, repair)
        self.assertEqual(Availability.objects.get_all_by_task(repair.name)[1].what, repair)

    def test_get_availability_all_by_task_ordered_by_date_ascendant_2(self):
        """ GIVEN 3 availabilities, 1 for Device Installation, 2 for Repair; WHEN requesting all availabilities for "Repair"; THEN 2 availabilities should be returned in ascendant order by schedule date for task "Repair" """

        loc_name = "Buenos Aires"
        l1 = Location.objects.create_location(loc_name)
        install = Task.objects.create_task("Device Installation", 30)
        repair = Task.objects.create_task("Repair", 30)
        now = datetime.now(timezone.utc)
        a3 = Availability.objects.create_availability(now + timedelta(days = 3), l1, install)
        a2 = Availability.objects.create_availability(now + timedelta(days = 1), l1, repair)
        a1 = Availability.objects.create_availability(now + timedelta(days = 2), l1, repair)
        self.assertEqual(len(Availability.objects.get_all_by_task(repair.name)), 2)
        self.assertIn(a1, Availability.objects.get_all_by_task(repair.name))
        self.assertIn(a2, Availability.objects.get_all_by_task(repair.name))
        self.assertTrue(Availability.objects.get_all_by_task(repair.name)[0].when < Availability.objects.get_all_by_task(repair.name)[1].when)
        self.assertEqual(Availability.objects.get_all_by_task(repair.name)[0].what, repair)
        self.assertEqual(Availability.objects.get_all_by_task(repair.name)[1].what, repair)

    def test_get_availability_all_by_task_ordered_by_date_ascendant_3(self):
        """ GIVEN 3 availabilities, 1 for Device Installation, 2 for Repair, 1 Repair is boooked; WHEN requesting all availabilities for "Repair"; THEN 1 availabilities should be returned in ascendant order by schedule date for task "Repair" """

        loc_name = "Buenos Aires"
        l1 = Location.objects.create_location(loc_name)
        install = Task.objects.create_task("Device Installation", 30)
        repair = Task.objects.create_task("Repair", 30)
        now = datetime.now(timezone.utc)
        a3 = Availability.objects.create_availability(now + timedelta(days = 3), l1, install)
        a2 = Availability.objects.create_availability(now + timedelta(days = 2), l1, repair)
        a1 = Availability.objects.create_availability(now + timedelta(days = 1), l1, repair)
        a1.book()
        self.assertEqual(len(Availability.objects.get_all_by_task(repair.name)), 1)
        self.assertEqual(Availability.objects.get_all_by_task(repair.name)[0], a2)
        self.assertEqual(Availability.objects.get_all_by_task(repair.name)[0].what, repair)

    def test_availability_serialize(self):
        loc_name = "Córdoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 30)
        now = datetime.now(timezone.utc)
        a1 = Availability.objects.create_availability(now + timedelta(days = 3), l1, t1)

        expected = {'id': 1, 'when': (now + timedelta(days = 3)).isoformat(), 'where': l1.json(), 'what': t1.json()}
        self.assertEqual(a1.json()["when"], (now + timedelta(days = 3)).isoformat())
        self.assertJSONEqual(json.dumps(a1.json()["where"]), json.dumps(l1.json()))
        self.assertJSONEqual(json.dumps(a1.json()["what"]), json.dumps(t1.json()))

    def test_availability_booked_initially_false(self):
        """ New availability should be not booked by default """
        loc_name = "Córdoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 30)
        now = datetime.now(timezone.utc)
        a1 = Availability.objects.create_availability(now + timedelta(days = 3), l1, t1)

        self.assertFalse(a1.booked)

    def test_availability_book(self):
        """ Given an availabiliy, when booked, then it is marked as booked """
        loc_name = "Córdoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 30)
        now = datetime.now(timezone.utc)
        a1 = Availability.objects.create_availability(now + timedelta(days = 3), l1, t1)
        a1.book()

        self.assertTrue(a1.booked)

    def test_availability_free(self):
        """ GIVEN a booked availabiliy; WHEN freed; THEN it is marked as not booked """
        loc_name = "Córdoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 30)
        now = datetime.now(timezone.utc)
        a1 = Availability.objects.create_availability(now + timedelta(days = 3), l1, t1)
        a1.book()
        self.assertTrue(a1.booked)
        a1.free()
        self.assertFalse(a1.booked)

    def test_get_availability_next_by_task_and_date(self):
        """ GIVEN 1 availability at Cordoba, tomorrow, for "Device Installation"; WHEN requesting next availabilities for "Device Installation" for tomorrow, THEN 1 availability should be returned at Cordoba, tomorrow for "Device Installation" """

        now = datetime.now(timezone.utc)
        tomorrow = now + timedelta(days = 1)
        loc_name = "Cordoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 30)
        a1 = Availability.objects.create_availability(tomorrow, l1, t1)
        result = Availability.objects.get_next_by_task_and_date(task_name, tomorrow)
        self.assertEqual(len(result), 1)
        availability = result[0]
        self.assertEqual(availability.when, tomorrow)
        self.assertEqual(availability.where.name, loc_name)
        self.assertEqual(availability.what.name, task_name)

    def test_get_availability_next_by_task_and_date_no_availabilities_at_date(self):
        """ GIVEN 1 availability at Cordoba, tomorrow + 1, for "Device Installation"; WHEN requesting next availabilities for "Device Installation" for today, THEN 0 availability should be returned """

        now = datetime.now(timezone.utc)
        tomorrow = now + timedelta(days = 1)
        loc_name = "Cordoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 30)
        a1 = Availability.objects.create_availability(tomorrow + timedelta(days = 1), l1, t1)
        result = Availability.objects.get_next_by_task_and_date(task_name, tomorrow)
        self.assertEqual(len(result), 0)

    def test_get_availability_next_by_task_and_date_no_more_availabilities_today(self):
        """ GIVEN 1 availability at Cordoba, now - 30min, for "Device Installation"; WHEN requesting next availabilities for "Device Installation" for today, THEN 0 availability should be returned """

        now = datetime.now(timezone.utc)
        loc_name = "Cordoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 60)
        a1 = Availability.objects.create_availability(now + timedelta(minutes = -30), l1, t1)
        result = Availability.objects.get_next_by_task_and_date(task_name, now)
        self.assertEqual(len(result), 0)

    def test_get_availability_next_by_task_and_date_1_availability_today(self):
        """ GIVEN 1 availability at Cordoba, now + 30min, for "Device Installation"; WHEN requesting next availabilities for "Device Installation" for today, THEN 1 availability should be returned """

        now = datetime.now(timezone.utc)
        loc_name = "Cordoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 60)
        a1 = Availability.objects.create_availability(now + timedelta(minutes = 30), l1, t1)
        result = Availability.objects.get_next_by_task_and_date(task_name, now)
        self.assertEqual(len(result), 1)
        availability = result[0]
        self.assertEqual(availability.when, now + timedelta(minutes = 30))
        self.assertEqual(availability.where.name, loc_name)
        self.assertEqual(availability.what.name, task_name)

    def test_get_availability_next_by_task_and_date_2_availability_today_ordered_ascending(self):
        """ GIVEN 2 availabilities at Cordoba, now + 30min and now + 60min, for "Device Installation"; WHEN requesting next availabilities for "Device Installation" for today, THEN 2 availabilities should be returned """

        now = datetime.now(timezone.utc)
        loc_name = "Cordoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 60)
        a1 = Availability.objects.create_availability(now + timedelta(minutes = 60), l1, t1)
        a2 = Availability.objects.create_availability(now + timedelta(minutes = 30), l1, t1)
        result = Availability.objects.get_next_by_task_and_date(task_name, now)
        self.assertEqual(len(result), 2)
        availability = result[0]
        self.assertEqual(availability.when, now + timedelta(minutes = 30))
        self.assertEqual(availability.where.name, loc_name)
        self.assertEqual(availability.what.name, task_name)
        availability = result[1]
        self.assertEqual(availability.when, now + timedelta(minutes = 60))
        self.assertEqual(availability.where.name, loc_name)
        self.assertEqual(availability.what.name, task_name)

    def test_get_availability_next_by_task_and_date_1_availability_today2(self):
        """ GIVEN 2 availabilities at Cordoba, now + 30min and now - 60min, for "Device Installation"; WHEN requesting next availabilities for "Device Installation" for today, THEN 1 availability should be returned for now + 30min"""

        now = datetime.now(timezone.utc)
        loc_name = "Cordoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 60)
        a1 = Availability.objects.create_availability(now + timedelta(minutes = 30), l1, t1)
        a2 = Availability.objects.create_availability(now + timedelta(minutes = -60), l1, t1)
        result = Availability.objects.get_next_by_task_and_date(task_name, now)
        self.assertEqual(len(result), 1)
        availability = result[0]
        self.assertEqual(availability.when, now + timedelta(minutes = 30))
        self.assertEqual(availability.where.name, loc_name)
        self.assertEqual(availability.what.name, task_name)

    def test_get_availability_next_by_task_and_date_none(self):
        """ GIVEN 2 availabilities at Cordoba, [day after tomorrow at 12:30] and [day after tomorrow at 11:00]; WHEN requesting next availabilities for "Device Installation" without a date; THEN 2 availabilites should be returned """

        afterTomorrow = datetime.now(timezone.utc) + timedelta(days=2)
        time1 = time(hour=11, minute=00, tzinfo=timezone.utc)
        time2 = time(hour=12, minute=30, tzinfo=timezone.utc)
        loc_name = "Cordoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 60)
        a1 = Availability.objects.create_availability(datetime.combine(afterTomorrow, time1), l1, t1)
        a2 = Availability.objects.create_availability(datetime.combine(afterTomorrow, time2), l1, t1)
        result = Availability.objects.get_next_by_task_and_date(task_name, None)
        self.assertEqual(len(result), 2)
        availability = result[0]
        self.assertEqual(availability.when, datetime.combine(afterTomorrow, time1))
        self.assertEqual(availability.where.name, loc_name)
        self.assertEqual(availability.what.name, task_name)
        availability = result[1]
        self.assertEqual(availability.when, datetime.combine(afterTomorrow, time2))
        self.assertEqual(availability.where.name, loc_name)
        self.assertEqual(availability.what.name, task_name)

    def test_get_availability_next_by_task_and_date_none_2(self):
        """ GIVEN 2 availabilities at Cordoba, [yesterday + 30min] and [day after tomorrow - 60min]; WHEN requesting next availabilities for "Device Installation" without a date; THEN 1 availability should be returned (day after tomorrow)"""

        now = datetime.now(timezone.utc)
        loc_name = "Cordoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 60)
        a1 = Availability.objects.create_availability(now + timedelta(days=-1, minutes = 30), l1, t1)
        a2 = Availability.objects.create_availability(now + timedelta(days=2, minutes = -60), l1, t1)
        result = Availability.objects.get_next_by_task_and_date(task_name, None)
        self.assertEqual(len(result), 1)
        availability = result[0]
        self.assertEqual(availability.when, now + timedelta(days=2, minutes = -60))
        self.assertEqual(availability.where.name, loc_name)
        self.assertEqual(availability.what.name, task_name)

    def test_get_availability_next_by_task_and_date_none_3(self):
        """ GIVEN 2 availabilities at Cordoba, [now - 60min]; WHEN requesting next availabilities for "Device Installation" without a date; THEN 0 availabilities should be returned """

        now = datetime.now(timezone.utc)
        loc_name = "Cordoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 60)
        a2 = Availability.objects.create_availability(now + timedelta(minutes = -60), l1, t1)
        result = Availability.objects.get_next_by_task_and_date(task_name, None)
        self.assertEqual(len(result), 0)

    def test_get_availability_next_by_task_and_date_none_4(self):
        """ GIVEN 1 availability at Cordoba, [now + 60min]; WHEN requesting next availabilities for "Device Installation" without a date; THEN 1 availability should be returned """

        now = datetime.now(timezone.utc)
        loc_name = "Cordoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 60)
        a2 = Availability.objects.create_availability(now + timedelta(minutes = 60), l1, t1)
        result = Availability.objects.get_next_by_task_and_date(task_name, None)
        self.assertEqual(len(result), 1)
        availability = result[0]
        self.assertEqual(availability.when, now + timedelta(minutes = 60))
        self.assertEqual(availability.where.name, loc_name)
        self.assertEqual(availability.what.name, task_name)

    def test_get_availability_next_by_task_and_date_none_5(self):
        """ GIVEN 2 availabilities at Cordoba, [now - 30min] and [now + 60min]; WHEN requesting next availabilities for "Device Installation" without a date; THEN 1 availability should be returned [now + 60min] """

        now = datetime.now(timezone.utc)
        loc_name = "Cordoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 60)
        a1 = Availability.objects.create_availability(now + timedelta(minutes = -30), l1, t1)
        a2 = Availability.objects.create_availability(now + timedelta(minutes = 60), l1, t1)
        result = Availability.objects.get_next_by_task_and_date(task_name, None)
        self.assertEqual(len(result), 1)
        availability = result[0]
        self.assertEqual(availability.when, now + timedelta(minutes = 60))
        self.assertEqual(availability.where.name, loc_name)
        self.assertEqual(availability.what.name, task_name)

    def test_get_availability_next_by_task_and_date_none_6(self):
        """ GIVEN 2 availabilities at Cordoba, [now - 30min] and [tomorrow + 60min]; WHEN requesting next availabilities for "Device Installation" without a date; THEN 1 availability should be returned tomorrow + 60min] """

        now = datetime.now(timezone.utc)
        loc_name = "Cordoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 60)
        a1 = Availability.objects.create_availability(now + timedelta(minutes = -30), l1, t1)
        a2 = Availability.objects.create_availability(now + timedelta(days=1, minutes = 60), l1, t1)
        result = Availability.objects.get_next_by_task_and_date(task_name, None)
        self.assertEqual(len(result), 1)
        availability = result[0]
        self.assertEqual(availability.when, now + timedelta(days=1, minutes = 60))
        self.assertEqual(availability.where.name, loc_name)
        self.assertEqual(availability.what.name, task_name)

    def test_get_availability_next_by_task_and_date_none_7(self):
        """ GIVEN 3 availabilities at Cordoba, [now - 30min],[tomorrow + 60min],[day after tomorrow + 60min]; WHEN requesting next availabilities for "Device Installation" without a date; THEN 1 availability should be returned tomorrow + 60min] """

        now = datetime.now(timezone.utc)
        l1 = Location.objects.create_location("Cordoba")
        t1 = Task.objects.create_task("Device Installation", 60)
        a1 = Availability.objects.create_availability(now + timedelta(minutes = -30), l1, t1)
        a2 = Availability.objects.create_availability(now + timedelta(days=1, minutes = 60), l1, t1)
        a2 = Availability.objects.create_availability(now + timedelta(days=2, minutes = 60), l1, t1)
        result = Availability.objects.get_next_by_task_and_date(t1.name, None)
        self.assertEqual(len(result), 1)
        availability = result[0]
        self.assertEqual(availability.when, now + timedelta(days=1, minutes = 60))
        self.assertEqual(availability.where.name, l1.name)
        self.assertEqual(availability.what.name, t1.name)

    def test_get_availability_all_by_location_and_date_tomorrow(self):
        """ GIVEN 1 availability at Cordoba, tomorrow, for "Device Installation", WHEN requesting all availabilities for "Device Installation" for tomorrow at Córdoba, THEN 1 availability should be returned at Cordoba, tomorrow for "Device Installation" """

        now = datetime.now(timezone.utc)
        tomorrow = now + timedelta(days = 1)
        l1 = Location.objects.create_location("Cordoba")
        t1 = Task.objects.create_task("Device Installation", 30)
        a1 = Availability.objects.create_availability(tomorrow, l1, t1)
        availabilities = Availability.objects.get_all_by_location_and_date(l1, tomorrow)
        self.assertEqual(len(availabilities), 1)
        availability = availabilities[0]
        self.assertEqual(availability.when, tomorrow)
        self.assertEqual(availability.where.name, l1.name)
        self.assertEqual(availability.what.name, t1.name)

    def test_get_availability_all_by_location_and_date_anotherdate(self):
        """ GIVEN 1 availability at Cordoba, tomorrow, for "Device Installation", WHEN requesting all availabilities for "Device Installation" for today at Córdoba, THEN 0 availabilities should be returned """

        now = datetime.now(timezone.utc)
        tomorrow = now + timedelta(days = 1)
        loc_name = "Cordoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 30)
        a1 = Availability.objects.create_availability(tomorrow, l1, t1)
        availabilities = Availability.objects.get_all_by_location_and_date(l1, now)
        self.assertEqual(len(availabilities), 0)

    def test_get_availability_all_by_location_and_date_tomorrow_elsewhere(self):
        """ GIVEN 1 availability at Cordoba, tomorrow, for "Device Installation", WHEN requesting all availabilities for "Device Installation" for today at Córdoba, THEN 0 availabilities should be returned """

        now = datetime.now(timezone.utc)
        tomorrow = now + timedelta(days = 1)
        l1 = Location.objects.create_location("Cordoba")
        l2 = Location.objects.create_location("Rosario")
        t1 = Task.objects.create_task("Device Installation", 30)
        a1 = Availability.objects.create_availability(tomorrow, l2, t1)
        availabilities = Availability.objects.get_all_by_location_and_date(l1, tomorrow)
        self.assertEqual(len(availabilities), 0)
