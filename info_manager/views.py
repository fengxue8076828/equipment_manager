from typing import Any, Dict
from django import http
from django.db.models import Count, Q
from django.urls import reverse
from django.shortcuts import redirect
from django.http.response import JsonResponse
from django.views.generic import (
    TemplateView,
    View,
    FormView,
    UpdateView,
    DeleteView,
    CreateView,
    ListView,
)
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import (
    CustomedAuthenticationForm,
    UserForm,
    UserCreateForm,
    EquipCategoryForm,
    WarehouseForm,
)
from django.contrib.auth.forms import PasswordChangeForm
from django.template.loader import render_to_string
from django.core import serializers
from .models import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.utils import timezone
from maintainance.models import DeviceMalfuntionRecord
from postsale.models import OutBound
from presale.models import Equipment

# Create your views here.


class CustomedLoginView(LoginView):
    form_class = CustomedAuthenticationForm


class MainPanelView(LoginRequiredMixin, TemplateView):
    template_name = "main_panel.html"

    def get_login_url(self):
        return reverse("login")


class MenuView(View):
    def get(self, request, *args, **kwargs):
        menu = request.user.role.modules.all()
        menu_data = serializers.serialize("json", menu)
        return JsonResponse({"menu": menu_data}, status=200)


class WelcomeView(TemplateView):
    template_name = "info-manager/welcome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        malfunction_records = DeviceMalfuntionRecord.objects.exclude(state="finished")
        if self.request.user.role.id == 4:
            malfunction_records = malfunction_records.filter(
                maintainer=self.request.user
            )
        malfunction_records_count = malfunction_records.count()
        context["malfunction_records_count"] = malfunction_records_count

        overdued_outbounds = OutBound.objects.filter(pay_state="unpaid").filter(
            pay_date__lte=timezone.now().date()
        )
        if self.request.user.role.id == 2:
            overdued_outbounds = overdued_outbounds.filter(
                outbound_operator=self.request.user
            )
        overdued_outbounds_count = overdued_outbounds.count()
        context["overdued_outbounds_count"] = overdued_outbounds_count

        low_device_number = (
            Equipment.objects.filter(is_active=True)
            .annotate(device_count=Count("devices", filter=Q(devices__is_sold=False)))
            .filter(device_count__lte=2)
            .count()
        )
        context["low_device_number"] = low_device_number
        return context

    def render_to_response(self, context, **response_kwargs):
        content = render_to_string(
            self.template_name, context=context, request=self.request
        )
        return JsonResponse({"content": content}, status=200)


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = UserForm(instance=self.request.user)
        context = {"form": form}
        content = render_to_string(
            "info/user-profile.html", context=context, request=self.request
        )
        return JsonResponse({"content": content}, status=200)

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST, request.FILES, instance=self.request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "success"}, status=200)
        return JsonResponse({"message": "failed"}, status=200)


class PasswordChangeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(self.request.user)
        context = {"form": form}
        content = render_to_string(
            "info/user-password.html", context=context, request=self.request
        )
        return JsonResponse({"content": content}, status=200)

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "success"}, status=200)
        else:
            context = {"form": form}
            content = render_to_string(
                "info/user-password.html", context=context, request=self.request
            )
            return JsonResponse({"content": content}, status=200)


class PasswordResetView(View):
    def get(self, request, *args, **kwargs):
        user_id = self.kwargs["id"]
        user = User.objects.get(id=user_id)
        user.set_password("123456")
        user.save()
        return JsonResponse({"message": "success"}, status=200)


class UserCreateView(FormView):
    def get(self, request, *args, **kwargs):
        form = UserCreateForm()
        context = {"form": form}
        content = render_to_string(
            "info-manager/user-create.html", context=context, request=self.request
        )
        return JsonResponse({"content": content}, status=200)

    def post(self, request, *args, **kwargs):
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            instance = form.save()
            instance.set_password("123456")
            instance.is_active = True
            messages.add_message(self.request, messages.SUCCESS, "更新成功！")
            instance.save()
            form = UserCreateForm()
        context = {"form": form}
        content = render_to_string(
            "info-manager/user-create.html", context=context, request=self.request
        )
        return JsonResponse({"content": content}, status=200)


class UserListView(ListView):
    model = User
    context_object_name = "users"
    paginate_by = 10

    def get_queryset(self):
        self.roles = Role.objects.all()
        if self.kwargs["role_id"] == "-1":
            queryset = User.objects.filter(is_active=True)
        else:
            queryset = User.objects.filter(is_active=True).filter(
                role__id=self.kwargs["role_id"]
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"roles": self.roles, "role_id": int(self.kwargs["role_id"])})
        return context

    def render_to_response(self, context, **response_kwargs):
        content = render_to_string(
            "info-manager/user-list.html", context=context, request=self.request
        )
        return JsonResponse({"content": content}, status=200)

    # def get(self,request,*args,**kwargs):
    #     roles=Role.objects.all()
    #     if kwargs['role_id']=='-1':
    #         users=User.objects.filter(is_active=True)
    #     else:
    #         users=User.objects.filter(is_active=True).filter(role__id=kwargs['role_id'])
    #     context={"users":users,"roles":roles,"role_id":int(kwargs['role_id'])}
    #     content=render_to_string("info-manager/user-list.html",context=context,request=self.request)
    #     return JsonResponse({"content":content},status=200)


class UserDeleteView(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs["id"])
        user.is_active = False
        user.save()
        roles = Role.objects.all()
        if kwargs["role_id"] == "-1":
            users = User.objects.filter(is_active=True)
        else:
            users = User.objects.filter(is_active=True).filter(
                role__id=kwargs["role_id"]
            )
        context = {"users": users, "roles": roles, "selected_role": kwargs["role_id"]}
        content = render_to_string(
            "info-manager/user-list.html", context=context, request=self.request
        )
        return JsonResponse({"content": content}, status=200)


class RoleListView(View):
    def get(self, request, *args, **kwargs):
        roles = Role.objects.all()
        parent_modules = Module.objects.filter(parent_module=None)
        child_modules = Module.objects.exclude(parent_module=None)
        if self.request.GET.get("role_id"):
            role_id = self.request.GET.get("role_id")
        else:
            role_id = request.user.role.id
        print("*************", role_id)
        current_parent_modules = Module.objects.filter(parent_module=None).filter(
            role__id=role_id
        )
        current_child_modules = Module.objects.exclude(parent_module=None).filter(
            role__id=role_id
        )

        context = {
            "roles": roles,
            "parent_modules": parent_modules,
            "child_modules": child_modules,
            "current_parent_modules": current_parent_modules,
            "current_child_modules": current_child_modules,
            "role_id": int(role_id),
        }
        content = render_to_string(
            "info-manager/role-list.html", context=context, request=self.request
        )
        return JsonResponse({"content": content}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class RoleUpdateView(View):
    def post(self, request, *args, **kwargs):
        role_id = request.POST["role_id"]
        module_ids = request.POST["modules"]
        role = Role.objects.get(id=role_id)
        role.modules.clear()
        for module_id in module_ids.split(","):
            module = Module.objects.get(id=module_id)
            role.modules.add(module)
        role.save()

        roles = Role.objects.all()
        parent_modules = Module.objects.filter(parent_module=None)
        child_modules = Module.objects.exclude(parent_module=None)
        current_parent_modules = Module.objects.filter(parent_module=None).filter(
            role__id=role_id
        )
        current_child_modules = Module.objects.exclude(parent_module=None).filter(
            role__id=role_id
        )
        print("************", parent_modules)
        context = {
            "roles": roles,
            "parent_modules": parent_modules,
            "child_modules": child_modules,
            "current_parent_modules": current_parent_modules,
            "role_id": role_id,
            "current_child_modules": current_child_modules,
        }
        content = render_to_string(
            "info-manager/role-list.html", context=context, request=self.request
        )
        return JsonResponse({"content": content}, status=200)


class EquipCategoryListView(View):
    def get(self, request, *args, **kwargs):
        if "parent_id" not in kwargs:
            equip_categories = EquipCategory.objects.filter(parent=None)
            context = {"equip_categories": equip_categories}
            content = render_to_string(
                "info-manager/category-list-template.html",
                context=context,
                request=request,
            )
        else:
            parent_id = kwargs["parent_id"]
            equip_categories = EquipCategory.objects.filter(parent__id=parent_id)
            context = {"equip_categories": equip_categories}
            content = render_to_string(
                "info-manager/category-list.html", context=context, request=request
            )
        return JsonResponse({"content": content}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class EquipCategoryUpdateView(UpdateView):
    form_class = EquipCategoryForm
    queryset = EquipCategory.objects.all()

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        form = self.form_class(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            messages.add_message(self.request, messages.SUCCESS, "更新成功！")
            return JsonResponse({"message": "success"}, status=200)
        return JsonResponse({"message": "fail"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class EquipCategoryDeleteView(DeleteView):
    queryset = EquipCategory.objects.all()

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            instance = self.get_object()
            children = EquipCategory.objects.filter(parent=instance)
            equipments = instance.equipment_set.all()
            if children:
                return JsonResponse({"message": "has-children"}, status=200)
            if equipments:
                return JsonResponse({"message": "has-equipments"}, status=200)
            instance.delete()
            return JsonResponse({"message": "success"}, status=200)
        return JsonResponse({"message": "fail"}, status=200)


class EuipCategoryCreateView(CreateView):
    form_class = EquipCategoryForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {"form": form}

        content = render_to_string(
            "info-manager/category-create.html", context=context, request=self.request
        )
        return JsonResponse({"content": content}, status=200)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "success"}, status=200)
        return JsonResponse({"message": "fail"}, status=200)


class WarehouseListView(View):
    def get(self, request, *args, **kwargs):
        warehouses = Warehouse.objects.all()
        context = {"warehouses": warehouses}
        content = render_to_string(
            "info-manager/warehouse-list.html", context=context, request=request
        )
        return JsonResponse({"content": content}, status=200)


class WarehouseCreateView(CreateView):
    form_class = WarehouseForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {"form": form}

        content = render_to_string(
            "info-manager/warehouse-create.html", context=context, request=self.request
        )
        return JsonResponse({"content": content}, status=200)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "success"}, status=200)
        return JsonResponse({"message": "fail"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class WarehouseUpdateView(UpdateView):
    form_class = WarehouseForm
    queryset = Warehouse.objects.all()

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        form = self.form_class(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            messages.add_message(self.request, messages.SUCCESS, "更新成功！")
            return JsonResponse({"message": "success"}, status=200)
        return JsonResponse({"message": "fail"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class WarehouseDeleteView(DeleteView):
    queryset = Warehouse.objects.all()

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            instance = self.get_object()
            if instance.devices.all():
                return JsonResponse({"message": "has-devices"}, status=200)
            instance.delete()
            return JsonResponse({"message": "success"}, status=200)
        return JsonResponse({"message": "fail"}, status=200)
