from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import gettext as _
from datetime import datetime, timezone
import json
import sys
from .models import Task, Availability, Booking, User, Location
from policorp.lib.schedule import Schedule

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "policorp/login.html")

    return render(request, "policorp/index.html");

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None and user.is_supervisor:
            login(request, user)
            return HttpResponseRedirect(reverse("policorp:index"))
        else:
            return render(request, "policorp/login.html", {
                "message": _("Invalid username and/or password")
            })
    else:
        return render(request, "policorp/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("policorp:index"))

def tasks(request):

    # Only GET requests allowed
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)

    return JsonResponse([t.json() for t in Task.objects.get_all()], safe=False)

def availabilities(request, taskid):

    # Only GET requests allowed
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)

    t = Task.objects.get(pk=taskid)
    availabilities = Availability.objects.get_next_by_task_and_date(t.name, None)

    return JsonResponse([a.json() for a in availabilities], status=200, safe=False)

def dailyavailabilities(request, taskid, date):

    # Only GET requests allowed
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)

    t = Task.objects.get(pk=taskid)
    availabilities = Availability.objects.get_next_by_task_and_date(t.name, datetime.strptime(date, "%Y%m%d"))

    return JsonResponse([a.json() for a in availabilities], status=200, safe=False)

def book(request, availabilityid):

    # Only POST requests allowed
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Only authenticated users
    if not request.user.is_authenticated:
        return JsonResponse({"error": _("Unauthorized")}, status=401)

    availability = Availability.objects.get(pk=availabilityid)
    booking = Booking.objects.book(availability, request.user)

    return JsonResponse(booking.json(), status=201)

def myschedule(request):

    # Only GET requests allowed
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)

    # Only authenticated users
    if not request.user.is_authenticated:
        return JsonResponse({"error": _("Unauthorized")}, status=401)

    bookings = Booking.objects.get_by_user(request.user)

    return JsonResponse([b.json() for b in bookings], safe=False)

def cancelbooking(request, bookingid):
    # Only POST requests allowed
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Only authenticated users
    if not request.user.is_authenticated:
        return JsonResponse({"error": _("Unauthorized")}, status=401)

    b = Booking.objects.get(pk=bookingid)
    location = b.availability.where
    user = User.objects.get(username=request.user.username)

    # Only users who booked or that supervise the location are allowed to cancel
    if request.user != b.user and location not in user.get_supervised_locations():
        return JsonResponse({"error": _("Unauthorized")}, status=401)

    b = b.cancel()

    return JsonResponse (b.json(),status=201)

def mysupervisedlocations(request):
    # Only GET requests allowed
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)

    # Only authenticated users
    if not request.user.is_authenticated:
        return JsonResponse({"error": _("Unauthorized")}, status=401)

    user = User.objects.get(username=request.user.username)

    if not user.is_supervisor:
        return JsonResponse({"error": _("Unauthorized")}, status=401)

    return JsonResponse([l.json() for l in user.get_supervised_locations()], safe=False)

def locationschedule(request, locationid, date):
    # Only GET requests allowed
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)

    # Only authenticated, supervisor users allowed
    if not request.user.is_authenticated:
        return JsonResponse({"error": _("Unauthorized")}, status=401)

    user = User.objects.get(username=request.user.username)

    if not user.is_supervisor:
        return JsonResponse({"error": _("Unauthorized")}, status=401)

    location = Location.objects.get(pk=locationid)

    if user not in location.supervisors.all():
        return JsonResponse({"error": _("Unauthorized")}, status=401)

    dateObj = datetime.strptime(date, "%Y%m%d")
    bookings = Booking.objects.get_by_location_and_date(location, dateObj)
    availabilities = Availability.objects.get_all_by_location_and_date(location, dateObj)
    sch = Schedule(dateObj.date(), location, availabilities, bookings)

    return JsonResponse(sch.json(), safe=False)

def createavailabilitysingle(request):
    # Only POST requests allowed
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Only authenticated, supervisor users allowed
    if not request.user.is_authenticated:
        return JsonResponse({"error": _("Unauthorized")}, status=401)

    user = User.objects.get(username=request.user.username)

    if not user.is_supervisor:
        return JsonResponse({"error": _("Unauthorized")}, status=401)

    data = json.loads(request.body)

    # User needs to be supervising requested location
    location = Location.objects.get(pk=data.get("locationid"))
    if user not in location.supervisors.all():
        return JsonResponse({"error": _("Unauthorized")}, status=401)

    when = datetime.fromisoformat(data.get("when"))
    task = Task.objects.get(pk=data.get("taskid"))
    a = Availability.objects.create_availability(when, location, task)

    return JsonResponse(a.json(), safe=False, status=201)

def createavailabilities(request):
    # Only POST requests allowed
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Only authenticated, supervisor users allowed
    if not request.user.is_authenticated:
        return JsonResponse({"error": _("Unauthorized")}, status=401)

    user = User.objects.get(username=request.user.username)

    if not user.is_supervisor:
        return JsonResponse({"error": _("Unauthorized")}, status=401)

    data = json.loads(request.body)

    response = []

    for a in data:

        location = Location.objects.get(pk=a.get("locationid"))
        if user not in location.supervisors.all():
            response.append({
                "locationid": a.get("locationid"),
                "taskid": a.get("taskid"),
                "when": a.get("when"),
                "error": "Unauthorized"
            })
        else:
            when = datetime.fromisoformat(a.get("when"))
            task = Task.objects.get(pk=a.get("taskid"))
            a = Availability.objects.create_availability(when, location, task)
            response.append(a.json())

    return JsonResponse(response, safe=False, status=201)
