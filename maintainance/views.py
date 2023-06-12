from datetime import datetime
from typing import Any, Dict, Optional, Type
from django import http
from django.db import models
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import render
from django.views import View
from .models import MaintainanceRecord, DeviceMalfuntionRecord
from presale.models import Device
from django.views import generic
from presale.models import Device
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from .forms import DeviceMalfunctionRecordForm, MaintainanceRecordForm
from postsale.models import DeviceSold
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

# Create your views here.

User = get_user_model()


class DeviceMaintainanceListView(View):
    # def get(self,request,*args,**kwargs):
    #     devices = Device.objects().all()
    #     if request.user.role.id == 4:
    #         records = devices.filter(maintainer=request.user)
    pass


class DeviceListView(generic.ListView):
    template_name = "maintainance/device-list.html"
    context_object_name = "devices"
    paginate_by = 5

    def get_queryset(self):
        type = int(self.kwargs["type"])
        if not type:
            queryset = Device.objects.filter(is_sold=False)
        else:
            queryset = Device.objects.filter(is_sold=True)
        query_params = self.request.GET
        if query_params.get("device_name"):
            device_name = query_params.get("device_name")
            queryset = queryset.filter(equipment__name__contains=device_name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET
        if query_params.get("device_name"):
            context["device_name"] = query_params.get("device_name")
        else:
            context["device_name"] = ""
        context.update({"type": self.kwargs["type"]})
        return context

    def render_to_response(self, context, **response_kwargs):
        content = render_to_string(
            self.template_name, context=context, request=self.request
        )
        return JsonResponse({"content": content}, status=200)


class DeviceMalfunctionRecordCreate(generic.CreateView):
    model = DeviceMalfuntionRecord
    form_class = DeviceMalfunctionRecordForm
    template_name = "maintainance/device-malfunction-record-create.html"

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        device_id = self.kwargs["id"]
        device = Device.objects.get(id=device_id)
        if device.maintainer == None:
            return JsonResponse({"message": "fail"}, status=200)
        context = {"form": form, "device": device}
        content = render_to_string(
            self.template_name, context=context, request=self.request
        )
        return JsonResponse({"content": content}, status=200)

    def form_valid(self, form):
        device_id = self.kwargs["id"]
        device = Device.objects.get(id=device_id)
        form.instance.device = device
        obj = form.save()
        obj.dispatch_date = timezone.now().date()
        obj.maintainer = device.maintainer
        obj.save()
        if obj.device.is_sold:
            device_sold = DeviceSold.objects.get(device=obj.device)
            device_sold.state = "bad"
            device_sold.save()
        else:
            device = obj.device
            device.state = "bad"
            device.save()

        return JsonResponse({"message": "success"}, status=200)


class MalfunctionRecordListView(generic.ListView):
    context_object_name = "malfunction_records"
    template_name = "maintainance/malfunction-record-list.html"

    def get_queryset(self):
        queryset = DeviceMalfuntionRecord.objects.filter(
            device__maintainer=self.request.user
        ).exclude(state="finished")
        return queryset

    def render_to_response(self, context, **response_kwargs):
        content = render_to_string(
            self.template_name, context=context, request=self.request
        )
        return JsonResponse({"content": content}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class StartMaintainanceView(View):
    def patch(self, request, *args, **kwargs):
        malfunction_record_id = int(kwargs["malfunction_record_id"])
        malfunction_record = DeviceMalfuntionRecord.objects.get(
            id=malfunction_record_id
        )
        malfunction_record.state = "started"
        if malfunction_record.device.is_sold:
            device_sold = malfunction_record.device.device_sold
            device_sold.state = "maintaining"
            device_sold.save()

        else:
            device = malfunction_record.device
            device.state = "maintaining"
            device.save()
        malfunction_record.save()
        return JsonResponse({"message": "success"}, status=200)


class MaintainanceRecordCreateView(generic.CreateView):
    model = MaintainanceRecord
    form_class = MaintainanceRecordForm
    template_name = "maintainance/maintainance-record-create.html"

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        malfunction_record_id = self.kwargs["malfunction_record_id"]
        record = DeviceMalfuntionRecord.objects.get(id=malfunction_record_id)

        context = {"form": form, "record": record}
        content = render_to_string(
            self.template_name, context=context, request=self.request
        )
        return JsonResponse({"content": content}, status=200)

    def form_valid(self, form):
        malfunction_record_id = self.kwargs["malfunction_record_id"]
        malfunction_record = DeviceMalfuntionRecord.objects.get(
            id=malfunction_record_id
        )
        form.instance.malfunction_record = malfunction_record
        obj = form.save(commit=False)
        obj.date = timezone.now().date()
        obj.save()
        print("*******************", form.cleaned_data["is_finished"])
        if form.cleaned_data["is_finished"]:
            device = malfunction_record.device
            if device.is_sold:
                device_sold = device.device_sold
                device_sold.state = "good"
                device_sold.save()
            else:
                device.state = "ready_confirm"
            device.save()
            malfunction_record.state = "finished"
        else:
            malfunction_record.state = "started"
        malfunction_record.save()

        return JsonResponse({"message": "success"}, status=200)


class MaintainanceRecordListView(generic.ListView):
    template_name = "maintainance/maintainance-record-list.html"
    context_object_name = "maintainance_records"
    paginate_by = 5

    def get_queryset(self):
        malfunction_record_id = int(self.kwargs["malfunction_record_id"])
        self.malfunction_record = DeviceMalfuntionRecord.objects.get(
            id=malfunction_record_id
        )
        queryset = MaintainanceRecord.objects.filter(
            malfunction_record=self.malfunction_record
        ).order_by("date")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["malfunction_record"] = self.malfunction_record
        if self.request.GET.get("back_url"):
            context["back_url"] = self.request.GET.get("back_url")
        return context

    def render_to_response(self, context, **response_kwargs):
        content = render_to_string(
            self.template_name, context=context, request=self.request
        )
        return JsonResponse({"content": content}, status=200)


class MalfunctionRecordListQueryView(generic.ListView):
    context_object_name = "malfunction_records"
    template_name = "maintainance/malfunction-record-query-list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = DeviceMalfuntionRecord.objects.all()

        if self.request.user.role.id == 4:
            queryset = queryset.filter(maintainer=self.request.user)

        if "state" in self.request.GET and self.request.GET.get("state"):
            state = self.request.GET.get("state")
            queryset = queryset.filter(state=state)

        if "device_id" in self.request.GET and self.request.GET.get("device_id"):
            device_id = int(self.request.GET.get("device_id"))
            queryset = queryset.filter(device__id=device_id)

        if "equipment_name" in self.request.GET and self.request.GET.get(
            "equipment_name"
        ):
            equipment_name = self.request.GET.get("equipment_name")
            queryset = queryset.filter(device__equipment__name__contains=equipment_name)

        if "maintainer_id" in self.request.GET and self.request.GET.get(
            "maintainer_id"
        ):
            maintainer_id = int(self.request.GET.get("maintainer_id"))
            maintainer = User.objects.get(id=maintainer_id)
            queryset = queryset.filter(maintainer=maintainer)

        if "begin_date" in self.request.GET and self.request.GET.get("begin_date"):
            begin_date = self.request.GET.get("begin_date")
            begin_date = datetime.strptime(begin_date, "%Y-%m-%d").date()
            queryset = queryset.filter(dispatch_date__gte=begin_date)

        if "end_date" in self.request.GET and self.request.GET.get("end_date"):
            end_date = self.request.GET.get("end_date")
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            queryset = queryset.filter(dispatch_date__lte=end_date)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if "state" in self.request.GET and self.request.GET.get("state"):
            context["state"] = self.request.GET.get("state")

        if "device_id" in self.request.GET and self.request.GET.get("device_id"):
            context["device_id"] = self.request.GET.get("device_id")

        if "equipment_name" in self.request.GET and self.request.GET.get(
            "equipment_name"
        ):
            context["equipment_name"] = self.request.GET.get("equipment_name")
        if "maintainer_id" in self.request.GET and self.request.GET.get(
            "maintainer_id"
        ):
            context["maintainer_id"] = int(self.request.GET.get("maintainer_id"))

        if "begin_date" in self.request.GET and self.request.GET.get("begin_date"):
            begin_date = self.request.GET.get("begin_date")
            begin_date = datetime.strptime(begin_date, "%Y-%m-%d").date()
            context["begin_date"] = begin_date
        if "end_date" in self.request.GET and self.request.GET.get("end_date"):
            end_date = self.request.GET.get("end_date")
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            context["end_date"] = end_date

        maintainers = User.objects.filter(role__id=4)
        context["maintainers"] = maintainers
        context["back_url"] = self.request.build_absolute_uri()
        print("***************", context["back_url"])
        return context

    def render_to_response(self, context, **response_kwargs):
        content = render_to_string(
            self.template_name, context=context, request=self.request
        )
        return JsonResponse({"content": content}, status=200)
