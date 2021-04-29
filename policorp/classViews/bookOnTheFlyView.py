from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from policorp.serializers import BookingSerializer
from policorp.permissions import IsSupervisorUser
from policorp.models import Location

import sys

class BookOnTheFlyView(APIView):
    http_method_names = ['post']
    permission_classes = [permissions.IsAuthenticated&IsSupervisorUser]

    def post(self, request, format=None):

        # Check if IsSupervisorUser
        self.check_object_permissions(self.request, None)

        serializer = BookingSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):

            # Get location ID to check if user is a supervisor at that location
            data = serializer.validated_data
            location = data['availability']['where']

            if request.user not in location.supervisors.all():
                return Response(status=status.HTTP_403_FORBIDDEN)

            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
