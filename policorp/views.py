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
