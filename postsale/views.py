from django.shortcuts import render
from django.views import View
from presale.models import Device,Equipment
from info_manager.models import Warehouse
from .models import DeviceSold,Client,OutBound
from .forms import DeviceSoldForm,DeviceSoldUpdateForm
from django.template.loader import render_to_string
from django.http import JsonResponse,HttpResponse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.core import serializers
import datetime
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# Create your views here.

User = get_user_model()

class DeviceSoldCreateView(View):
    def get(self,request,*args,**kwargs):
        device_ids = self.request.GET.get("devices").split(",")
        devices = Device.objects.filter(id__in=device_ids)
        form = DeviceSoldForm()
        context = {"form":form,"devices":devices}
        content = render_to_string("postsale/device-sold-create.html",context=context,request=request)
        return JsonResponse({"content":content},status=200)
    
class OutBoundListView(View):
    def get(self,request,*args,**kwargs):
        
        outbounds = OutBound.objects.all()
        context = {}
        if("pay_state" in self.request.GET and self.request.GET.get("pay_state")):
            pay_state = self.request.GET.get("pay_state")
            outbounds = outbounds.filter(pay_state=pay_state)
            context.update({"pay_state":pay_state})
        if("begin_date" in self.request.GET and self.request.GET.get("begin_date")):
            begin_date = self.request.GET.get("begin_date")
            begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d").date()
            outbounds = outbounds.filter(outbound_date__gte=begin_date)
            context.update({"begin_date":begin_date})
        if("end_date" in self.request.GET and self.request.GET.get("end_date")):
            end_date = self.request.GET.get("end_date")
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
            outbounds = outbounds.filter(outbound_date__lte=end_date)
            context.update({"end_date":end_date})

        context.update({"outbounds":outbounds})
        content = render_to_string("postsale/outbound-list.html",context=context,request=request)
        return JsonResponse({"content":content},status=200)


class DeviceForSaleListView(View):
    def get(self,request,*args,**kwargs):
        devices = Device.objects.filter(state__contains="ready")
        context = {"devices":devices}
        content = render_to_string("postsale/device-forsale-list.html",context=context,request=request)
        return JsonResponse({"content":content},status=200)
    
class DeviceSoldUpdateView(View):
    def post(self,request,*args,**kwargs):
        form=DeviceSoldForm(self.request.POST,self.request.FILES)
        devices_ids = self.request.GET.get("devices").split(",")
        devices = Device.objects.filter(id__in=devices_ids)
        today_outbound = OutBound.objects.filter(outbound_date=timezone.now().date()).count()
        outbound_number=f'No.{timezone.now().date()}-{today_outbound+1}'

        if form.is_valid():
            outbound = OutBound.objects.create(outbound_number=outbound_number,outbound_operator=self.request.user,outbound_date=timezone.now().date(),**form.cleaned_data)
            outbound.save()

            for device in devices:
                device_sold = DeviceSold.objects.create(device=device,outbound=outbound,state="good",fix_address="")
                device.state="sold"
                device.warehouse=None
                device.save()
                device_sold.save()
            return JsonResponse({"message":"success"},status=200)

        return JsonResponse({"message":"failed"},status=200)

@method_decorator(csrf_exempt, name='dispatch')  
class DeviceSoldModifyView(View):
    def post(self,request,*args,**kwargs):
        device_sold_id = self.kwargs["device_sold_id"]
        instance = DeviceSold.objects.get(id=device_sold_id)
        form = DeviceSoldUpdateForm(self.request.POST)
        if form.is_valid():
            instance.state = form.cleaned_data["state"]
            instance.fix_address = form.cleaned_data["fix_address"]
            device = instance.device
            device.maintainer = form.cleaned_data["maintainer"]
            instance.save()
            device.save()
            return JsonResponse({"message":"success"},status=200)
        return JsonResponse({"message":"failed"},status=200)
    
class DeviceSoldListView(View):
    def get(self,request,*args,**kwargs):
        sold_devices = DeviceSold.objects.all()
        context={}
        template = "postsale/device-sold-list-outbound.html"
        if("outbound_id" in self.request.GET):
            outbound_id = self.request.GET.get("outbound_id")
            sold_devices.filter(outbound__id=outbound_id)                   
        else:
            maintainers = User.objects.filter(role__id=4)
            template = "postsale/device-sold-list.html"
            if "fix_address" in self.request.GET and self.request.GET.get("fix_address"):
                fix_address = self.request.GET.get("fix_address")
                print("*****************",fix_address)
                sold_devices = sold_devices.filter(fix_address__contains=fix_address)
                context.update({"fix_address":fix_address})
            if "buyer" in self.request.GET and self.request.GET.get("buyer"):
                buyer = self.request.GET.get("buyer")
                print("*****************",buyer)
                sold_devices = sold_devices.filter(outbound__buyer__name__contains=buyer)
                context.update({"buyer":buyer})
            if "equipment_name" in self.request.GET and self.request.GET.get("equipment_name"):
                equipment_name = self.request.GET.get("equipment_name")
                print("*****************",equipment_name)
                sold_devices = sold_devices.filter(device__equipment__name__contains=equipment_name)
                context.update({"equipment_name":equipment_name})
            if "state" in self.request.GET and self.request.GET.get("state"):
                state = self.request.GET.get("state")
                sold_devices = sold_devices.filter(state=state)
                context.update({"state":state})

        context.update({"sold_devices":sold_devices})
        context.update({"maintainers":maintainers})
        content = render_to_string(template,context=context,request=request)
        return JsonResponse({"content":content},status=200)
    
class DeviceOutboundPDFView(View):
    def get(self,request,*args,**kwargs):
        devices_ids = self.request.GET.get("devices").split(",")
        devices = Device.objects.filter(id__in=devices_ids)
        buyer_id = self.request.GET.get("buyer")
        buyer = Client.objects.get(id=buyer_id)


        today_outbound = OutBound.objects.filter(outbound_date=timezone.now().date()).count()

        outbound_number=f'No.{timezone.now().date()}-{today_outbound+1}'

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="出库单.pdf"'

        pdf = canvas.Canvas(response, pagesize=A4)

        pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))

        pdf.setFont('STSong-Light', 20)
        pdf.drawString(9*cm, (20+1.6+len(devices)*0.8+1.4)*cm, '出库单')
        pdf.setFont('STSong-Light', 11)
        pdf.drawString(0.5*cm, (20+1.6+len(devices)*0.8+0.4)*cm,  f'出库日期:  {timezone.now().date()}')
        pdf.drawString(6*cm, (20+1.6+len(devices)*0.8+0.4)*cm,  f'采购单位:  {buyer.name}')
        pdf.drawString(13.5*cm, (20+1.6+len(devices)*0.8+0.4)*cm, f'出库单号: {outbound_number}')
        pdf.setFont('STSong-Light', 14)
        table_data = [['设备名称','型号','金额','出库仓库','备注']]
        total_price=0.0
        for device in devices:
            table_data.append([device.equipment.name, device.equipment.model,device.equipment.price, device.warehouse.name, ''])
            total_price+=float(device.equipment.price)
        table_data.append(["合计:","",total_price])
        table = Table(table_data, colWidths=[3*cm, 2*cm, 2*cm, 3*cm,10*cm], rowHeights=0.8*cm)
        table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'STSong-Light'),
            ('FONTSIZE', (0,0), (-1,-1), 12),
            ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        table.wrapOn(pdf, 15*cm, 20*cm)
        table.drawOn(pdf, 0.5*cm, 20*cm)
        pdf.setFont('STSong-Light', 11)
        pdf.drawString(0.5*cm, 19.2*cm, f'库管: ')
        pdf.drawString(7.5*cm, 19.2*cm, f'出库人:  {request.user.real_name}')
        pdf.drawString(13.5*cm, 19.2*cm, '收货人:')


        pdf.setFillColorRGB(255,0,0)
        pdf.setFont('STSong-Light', 20)
        pdf.drawString(9*cm, (12+1.6+len(devices)*0.8+1.4)*cm, '出库单')
        pdf.setFont('STSong-Light', 11)
        pdf.drawString(0.5*cm, (12+1.6+len(devices)*0.8+0.4)*cm, f'出库日期:  {timezone.now().date()}')
        pdf.drawString(6*cm, (12+1.6+len(devices)*0.8+0.4)*cm,  f'采购单位:  {buyer.name}')
        pdf.drawString(13.5*cm, (12+1.6+len(devices)*0.8+0.4)*cm, f'出库单号: {outbound_number}')
        pdf.setFont('STSong-Light', 14)
        table_data = [['设备名称','型号','金额','出库仓库','备注']]
        total_price=0.0
        for device in devices:
            table_data.append([device.equipment.name, device.equipment.model,device.equipment.price, device.warehouse.name, ''])
            total_price+=float(device.equipment.price)
        table_data.append(["合计:","",total_price])
        table = Table(table_data, colWidths=[3*cm, 2*cm, 2*cm, 3*cm,10*cm], rowHeights=0.8*cm)
        table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'STSong-Light'),
            ('FONTSIZE', (0,0), (-1,-1), 12),
            ('TEXTCOLOR', (0,0), (-1,-1), colors.red),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 1, colors.red)
        ]))
        table.wrapOn(pdf, 15*cm, 12*cm)
        table.drawOn(pdf, 0.5*cm, 12*cm)
        pdf.setFont('STSong-Light', 11)
        pdf.drawString(0.5*cm, 11.2*cm, f'库管:  ')
        pdf.drawString(7.5*cm, 11.2*cm, f'出库人:  {request.user.real_name}')
        pdf.drawString(13.5*cm, 11.2*cm, '收货人:')


        pdf.setFillColorRGB(0,0,255)
        pdf.setFont('STSong-Light', 20)
        pdf.drawString(9*cm, (4+1.6+len(devices)*0.8+1.4)*cm, '出库单')
        pdf.setFont('STSong-Light', 11)
        pdf.drawString(0.5*cm, (4+1.6+len(devices)*0.8+0.4)*cm, f'出库日期:  {timezone.now().date()}')
        pdf.drawString(6*cm, (4+1.6+len(devices)*0.8+0.4)*cm,  f'采购单位:  {buyer.name}')
        pdf.drawString(13.5*cm, (4+1.6+len(devices)*0.8+0.4)*cm, f'出库单号:  {outbound_number}')
        pdf.setFont('STSong-Light', 14)
        table_data = [['设备名称','型号','金额','出库仓库','备注']]
        total_price=0.0
        for device in devices:
            table_data.append([device.equipment.name, device.equipment.model,device.equipment.price, device.warehouse.name, ''])
            total_price+=float(device.equipment.price)
        table_data.append(["合计:","",total_price])
        table = Table(table_data, colWidths=[3*cm, 2*cm, 2*cm, 3*cm,10*cm], rowHeights=0.8*cm)
        table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'STSong-Light'),
            ('FONTSIZE', (0,0), (-1,-1), 12),
            ('TEXTCOLOR', (0,0), (-1,-1), colors.blue),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 1, colors.blue)
        ]))
        table.wrapOn(pdf, 15*cm, 4*cm)
        table.drawOn(pdf, 0.5*cm, 4*cm)
        pdf.setFont('STSong-Light', 11)
        pdf.drawString(0.5*cm, 3.2*cm, f'库管:  ')
        pdf.drawString(7.5*cm, 3.2*cm, f'出库人:  {request.user.real_name}')
        pdf.drawString(13.5*cm, 3.2*cm, '收货人:')

        pdf.showPage()
        pdf.save()
        
        return response