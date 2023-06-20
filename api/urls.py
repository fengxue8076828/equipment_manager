from django.urls import path
from .views import (
    ApiDeviceList,
    ApiDeviceDetail,
    ApiMalfunctionRecordList,
    ApiMalfunctionRecordDetail,
    ApiMaintainanceRecordList,
)

app_name = "api"
urlpatterns = [
    path("getDeviceList/", ApiDeviceList.as_view(), name="getDeviceList"),
    path("getDevice/<int:pk>/", ApiDeviceDetail.as_view(), name="getDevice"),
    path(
        "getMalfunctionRecordList/",
        ApiMalfunctionRecordList.as_view(),
        name="getMalfunctionRecordList",
    ),
    path(
        "getMalfuntionRecordDetail/<int:pk>",
        ApiMalfunctionRecordDetail.as_view(),
        name="getMalfunctionRecordDetail",
    ),
    path(
        "getMaintainanceList/<int:malfunction_id>/",
        ApiMaintainanceRecordList.as_view(),
        name="getMaintainanceList",
    ),
]
