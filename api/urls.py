from django.urls import path
from .views import (
    ApiDeviceDetail,
    ApiMalfunctionRecordList,
    ApiMalfunctionRecordDetail,
    ApiMaintainanceRecordList,
    ApiWarehouseList,
    ApiMaintainerList,
    ApiDevicesByWarehouse,
    ApiMalfunctionCreate,
)

app_name = "api"
urlpatterns = [
    path("getWarehouseList/", ApiWarehouseList.as_view(), name="getWarehouserList"),
    path("getMaintainerList/", ApiMaintainerList.as_view(), name="getMaintainerList"),
    path("getDevice/<int:pk>/", ApiDeviceDetail.as_view(), name="getDevice"),
    path(
        "getDevicesByWarehouse/<int:warehouseId>/",
        ApiDevicesByWarehouse.as_view(),
        name="getDevicesByWarehouse",
    ),
    path(
        "createMalfunctionRecord/<int:deviceId>/",
        ApiMalfunctionCreate.as_view(),
        name="createMalfunctionRecord",
    ),
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
        "getMaintainanceList/<int:malfunction_id>/<int:finished>/",
        ApiMaintainanceRecordList.as_view(),
        name="getMaintainanceList",
    ),
]
