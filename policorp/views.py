from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Task, Availability

# Create your views here.
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
    availabilities = Availability.objects.get_all_by_task(t.name)

    return JsonResponse([a.json() for a in availabilities], status=200, safe=False)

def book(request, availabiliyid):
    return HttpResponse(status=201)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")