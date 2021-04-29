from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from policorp.serializers import BookingSerializer

class BookOnTheFlyView(APIView):
    http_method_names = ['post']

    def post(self, request, format=None):

        serializer = BookingSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):

            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
