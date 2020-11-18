from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Task

# Create your views here.
def tasks(request):

    # Only GET requests allowed
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)

    return JsonResponse([t.json() for t in Task.objects.get_all()], safe=False)
