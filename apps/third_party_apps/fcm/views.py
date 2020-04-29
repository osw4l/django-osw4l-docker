from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers
from .fcm import FCMMessage
from .settings import get_device_model

Device = get_device_model()


# url: /devices/
class DeviceList(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = serializers.DeviceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # Url Filters
        self.queryset = self.queryset.filter(user=self.request.user)
        return self.queryset

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context=self.request)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=self.request.user)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED)


# url: /devices/{id}/
class DeviceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = serializers.DeviceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # Url Filters
        self.queryset = self.queryset.get(user=self.request.user,
                                          pk=self.kwargs['pk'])
        return self.queryset

    def get_object(self, *args, **kwargs):
        try:
            return self.get_queryset()
        except Device.DoesNotExist:
            raise NotFound(detail=None)

    def put(self, request, *args, **kwargs):
        device = self.get_object()
        serializer = self.serializer_class(device, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data,
                            status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        device = self.get_object()
        device.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# url: /fcm/send/
class FCMList(generics.CreateAPIView):
    serializer_class = serializers.FCMSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            fcm = FCMMessage()
            resp = fcm.send(serializer.data['sender'],
                            **serializer.data['data'])
            try:
                data = resp.json()
            except ValueError:
                data = resp.reason
            return Response(status=resp.status_code, data=data)
