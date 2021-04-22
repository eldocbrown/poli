from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.http import Http404

from policorp.serializers import UserSerializer
from policorp.permissions import IsSameUser, IsSupervisorUser
from policorp.models import User

class UserView(APIView):
    http_method_names = ['get']
    permission_classes = [permissions.IsAuthenticated&(IsSupervisorUser|IsSameUser)]

    def get_object(self, username):
        try:
            requestedUser = User.objects.get(username=username)
            self.check_object_permissions(self.request, requestedUser)
            return requestedUser
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username, format=None):
        user = self.get_object(username)
        serializer = UserSerializer(user)
        return Response(serializer.data)
