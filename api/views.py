from django.shortcuts import render
from rest_framework import generics
from presale.models import Device
from maintainance.models import DeviceMalfuntionRecord, MaintainanceRecord
from dj_rest_auth.views import LoginView
from .serializers import (
    DeviceSerializer,
    DeviceMaintainanceRecordSerializer,
    MaintainanceRecordSerializer,
)
from info_manager.models import Role


# Create your views here.


class ApiDeviceList(generics.ListAPIView):
    queryset = Device.objects.filter(is_sold=False)
    serializer_class = DeviceSerializer


class ApiDeviceDetail(generics.RetrieveUpdateAPIView):
    queryset = Device.objects.filter(is_sold=False)
    serializer_class = DeviceSerializer


class ApiMalfunctionRecordList(generics.ListAPIView):
    serializer_class = DeviceMaintainanceRecordSerializer

    def get_queryset(self):
        queryset = DeviceMalfuntionRecord.objects.filter(
            maintainer=self.request.user
        ).exclude(state="finished")


class ApiMalfunctionRecordDetail(generics.RetrieveUpdateAPIView):
    serializer_class = DeviceMaintainanceRecordSerializer

    def get_queryset(self):
        queryset = DeviceMalfuntionRecord.objects.filter(
            maintainer=self.request.user
        ).exclude(state="finished")
        return queryset


class ApiMaintainanceRecordList(generics.ListCreateAPIView):
    serializer_class = MaintainanceRecordSerializer

    def get_queryset(self):
        malfunction_id = int(self.kwargs["malfunction_id"])
        self.malfunction_record = DeviceMalfuntionRecord.get(id=malfunction_id)
        queryset = MaintainanceRecord.objects.filter(
            malfunction_record=self.malfunction_record
        )
        return queryset

    def perform_create(self, serializer):
        instance = serializer.save(commmit=False)
        instance.malfunction_record = self.malfunction_record
        instance.save()


class ApiLoginView(LoginView):
    def get_response(self):
        response = super().get_response()
        role_id = self.user.role.id
        data = response.data
        data["role"] = role_id
        response.data = data
        return response
