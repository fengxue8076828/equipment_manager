from django.urls import path
from .views import (
    DeviceListView,
    DeviceMalfunctionRecordCreate,
    MalfunctionRecordListView,
    StartMaintainanceView,
    MaintainanceRecordCreateView,
    MaintainanceRecordListView,
    MalfunctionRecordListQueryView,
)

app_name = "maintainance"
urlpatterns = [
    path("device-list/<type>/", DeviceListView.as_view(), name="device-list"),
    path(
        "device-malfunction-record-create/<int:id>/",
        DeviceMalfunctionRecordCreate.as_view(),
        name="device-malfunction-record-create",
    ),
    path(
        "malfunction-record-list/",
        MalfunctionRecordListView.as_view(),
        name="malfunction-record-list",
    ),
    path(
        "start-maintainance/<malfunction_record_id>/",
        StartMaintainanceView.as_view(),
        name="start-maintainance",
    ),
    path(
        "maintainance-record-create/<malfunction_record_id>/",
        MaintainanceRecordCreateView.as_view(),
        name="maintainance-record-create",
    ),
    path(
        "maintainance-record-list/<malfunction_record_id>/",
        MaintainanceRecordListView.as_view(),
        name="maintainance-record-list",
    ),
    path(
        "malfunction-record-query-list/",
        MalfunctionRecordListQueryView.as_view(),
        name="malfunction-record-query-list",
    ),
]
