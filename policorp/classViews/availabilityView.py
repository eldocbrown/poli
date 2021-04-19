from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.http import Http404

from policorp.serializers import AvailabilitySerializer
from policorp.permissions import IsLocationSupervisorOrReadOnly
from policorp.models import Availability


class AvailabilityView(APIView):
    http_method_names = ['delete']
    permission_classes = [IsLocationSupervisorOrReadOnly]

    def get_object(self, availabilityid):
        try:
            obj = Availability.objects.get(pk=availabilityid)
            self.check_object_permissions(self.request, obj)
            return obj
        except Availability.DoesNotExist:
            raise Http404

    def delete(self, request, availabilityid, format=None):
        a = self.get_object(availabilityid)
        if not a.booked:
            a.delete()
        else:
            return Response(data={"detail": "Availability is already booked."}, status=status.HTTP_409_CONFLICT)
        return Response(status=status.HTTP_204_NO_CONTENT)
