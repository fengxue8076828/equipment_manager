from django.shortcuts import render
from rest_framework import generics
from presale.models import Device
from maintainance.models import DeviceMalfuntionRecord, MaintainanceRecord
from info_manager.models import Warehouse
from dj_rest_auth.views import LoginView
from .serializers import (
    DeviceSerializer,
    DeviceMalfunctionRecordSerializer,
    MaintainanceRecordSerializer,
    WarehouseSerializer,
    UserSerializer,
)
from info_manager.models import Role
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status

from django.utils import timezone

# Create your views here.

User = get_user_model()


# new
@permission_classes([IsAuthenticated])
class ApiWarehouseList(generics.ListAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


# new
@permission_classes([IsAuthenticated])
class ApiMaintainerList(generics.ListAPIView):
    queryset = User.objects.filter(role__id=4)
    serializer_class = UserSerializer


@permission_classes([IsAuthenticated])
class ApiDevicesByWarehouse(generics.ListAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        warehouse_id = self.kwargs.get("warehouseId")
        queryset = Device.objects.filter(warehouse__id=warehouse_id).select_related(
            "equipment"
        )
        return queryset


@permission_classes([IsAuthenticated])
class ApiDeviceDetail(generics.RetrieveUpdateAPIView):
    queryset = Device.objects.filter(is_sold=False).select_related("equipment")
    serializer_class = DeviceSerializer


# new
@permission_classes([IsAuthenticated])
class ApiMalfunctionCreate(generics.CreateAPIView):
    model = DeviceMalfuntionRecord
    serializer_class = DeviceMalfunctionRecordSerializer

    def perform_create(self, serializer):
        deviceId = self.kwargs["deviceId"]
        device = Device.objects.get(id=deviceId)
        serializer.save(
            operator=self.request.user,
            device=device,
            maintainer=device.maintainer,
            dispatch_date=timezone.now().date(),
        )

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     user = self.request.user
    #     serializer.device = self.device
    #     serializer.operator = user
    #     serializer.maintainer = self.maintainer
    #     serializer.dispatch_date = timezone.now().date()

    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(
    #         serializer.data, status=status.HTTP_201_CREATED, headers=headers
    #     )

    def post(self, request, *args, **kwargs):
        device_id = self.kwargs["deviceId"]
        self.device = Device.objects.get(id=device_id)
        self.maintainer = self.device.maintainer
        if self.maintainer == None:
            return Response({"message": "no maintainer"}, status=401)
        self.device.state = "bad"
        self.device.save()
        return self.create(request, *args, **kwargs)


@permission_classes([IsAuthenticated])
class ApiMalfunctionRecordList(generics.ListAPIView):
    serializer_class = DeviceMalfunctionRecordSerializer

    def get_queryset(self):
        queryset = DeviceMalfuntionRecord.objects.filter(
            maintainer=self.request.user
        ).exclude(state="finished")
        return queryset


@permission_classes([IsAuthenticated])
class ApiMalfunctionRecordDetail(generics.RetrieveUpdateAPIView):
    serializer_class = DeviceMalfunctionRecordSerializer

    def get_queryset(self):
        queryset = DeviceMalfuntionRecord.objects.filter(
            maintainer=self.request.user
        ).exclude(state="finished")
        return queryset


@permission_classes([IsAuthenticated])
class ApiMaintainanceRecordList(generics.ListCreateAPIView):
    serializer_class = MaintainanceRecordSerializer

    def get_queryset(self):
        malfunction_id = int(self.kwargs["malfunction_id"])
        malfunction_record = DeviceMalfuntionRecord.objects.get(id=malfunction_id)
        queryset = MaintainanceRecord.objects.filter(
            malfunction_record=malfunction_record
        )
        return queryset

    def perform_create(self, serializer):
        malfunction_id = int(self.kwargs["malfunction_id"])
        finished = int(self.kwargs["finished"])
        malfunction_record = DeviceMalfuntionRecord.objects.get(id=malfunction_id)
        device = malfunction_record.device
        if finished == 0:
            device.state = "maintaining"
            malfunction_record.state = "started"
        elif finished == 1:
            device.state = "ready_excellent"
            malfunction_record.state = "finished"
        malfunction_record.save()
        device.save()
        serializer.save(
            malfunction_record=malfunction_record,
            date=timezone.now().date(),
        )


class ApiLoginView(LoginView):
    def get_response(self):
        response = super().get_response()
        role_id = self.user.role.id
        data = response.data
        data["role"] = role_id
        data["user"] = self.user.real_name
        response.data = data
        return response
