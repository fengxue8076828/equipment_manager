from django.urls import path
from .views import (
    UserCreateView,
    UserListView,
    UserDeleteView,
    RoleListView,
    RoleUpdateView,
    EquipCategoryListView,
    EquipCategoryUpdateView,
    EquipCategoryDeleteView,
    EuipCategoryCreateView,
    WarehouseListView,
    WarehouseCreateView,
    WarehouseUpdateView,
    WarehouseDeleteView,
    PasswordResetView,
    WelcomeView,
)

app_name = "info_manager"
urlpatterns = [
    path("welcome/", WelcomeView.as_view(), name="welcome"),
    path("user-create/", UserCreateView.as_view(), name="user-create"),
    path("user-list/<role_id>/", UserListView.as_view(), name="user-list"),
    path("user-delete/<id>/<role_id>", UserDeleteView.as_view(), name="user-delete"),
    path("reset-password/<id>/", PasswordResetView.as_view(), name="reset-password"),
    path("role-list/", RoleListView.as_view(), name="role-list"),
    path("role-update/", RoleUpdateView.as_view(), name="role-update"),
    path("category-list/", EquipCategoryListView.as_view(), name="category-list"),
    path(
        "category-list/<parent_id>/",
        EquipCategoryListView.as_view(),
        name="category-list",
    ),
    path(
        "category-update/<pk>/",
        EquipCategoryUpdateView.as_view(),
        name="category-update",
    ),
    path(
        "category-delete/<pk>/",
        EquipCategoryDeleteView.as_view(),
        name="category-delete",
    ),
    path("category-create/", EuipCategoryCreateView.as_view(), name="category-create"),
    path("warehouse-list/", WarehouseListView.as_view(), name="warehouse-list"),
    path("warehouse-create/", WarehouseCreateView.as_view(), name="warehouse-create"),
    path(
        "warehouse-update/<pk>/", WarehouseUpdateView.as_view(), name="warehouse-update"
    ),
    path(
        "warehouse-delete/<pk>/", WarehouseDeleteView.as_view(), name="warehouse-delete"
    ),
]
