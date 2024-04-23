from django.shortcuts import render
from .serializers import SingUpSeializer
from rest_framework.views import APIView
from rest_framework.response import Response


class SingUpApiView(APIView):
    def post(self, request):
        serializer = SingUpSeializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



