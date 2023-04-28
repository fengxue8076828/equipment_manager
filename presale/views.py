from django.shortcuts import render
from django.views import View
from django.views.generic import UpdateView,DeleteView,DetailView
from .forms import EquipmentForm,InboundForm,DeviceUpdateForm,SupplierForm
from .models import Equipment,Device,Inbound,Supplier
from django.template.loader import render_to_string
from django.http import JsonResponse
from info_manager.models import EquipCategory,Warehouse
from django.core import serializers
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont


# Create your views here.

class InboundCreateView(View):
    def get(self,request,*args,**kwargs):
        equipments = Equipment.objects.all()
        form = InboundForm()
        context = {"equipments":equipments,"form":form}
        content = render_to_string("presale/inbound-create.html",context=context,request=request)
        return JsonResponse({"content":content},status=200)
    def post(self,request,*args,**kwargs):

        form = InboundForm(self.request.POST,self.request.FILES)
        if form.is_valid():
            # inbound = form.save(commit=False)
            
            # inbound.inbound_number=f'No.{timezone.now().date()}-{today_inbound+1}'
            # inbound.inbound_operator = self.request.user
            # inbound.date = timezone.now().date()
            # inbound.save()

            today_inbound = Inbound.objects.filter(inbound_date=timezone.now().date()).count()
            inbound = Inbound.objects.create(inbound_number=f'No.{timezone.now().date()}-{today_inbound+1}',inbound_operator=self.request.user,inbound_date=timezone.now().date(),**form.cleaned_data)
            inbound.save()

            for i in range(0,inbound.amount):
                device = Device.objects.create(equipment=inbound.equipment,supplier=inbound.supplier,warehouse=inbound.warehouse,inbound=inbound,state="ready_excellent")
                device.save()
            return JsonResponse({"message":"success"},status=200)
        return JsonResponse({"message":"fail"},status=200)
    
class EquipmentCreateView(View):
    def get(self,request,*args,**kwargs):     
        form = EquipmentForm()
        context = {"form":form}
        content = render_to_string("presale/equipment-create.html",context=context,request=request)
        return JsonResponse({"content":content},status=200)
    def post(self,requset,*args,**kwargs):
        form = EquipmentForm(self.request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"message":"success"},status=200)
        return JsonResponse({"message":"fail"},status=200)
    
class EquipmentUpdateView(UpdateView):
    queryset = Equipment.objects.all()
    form_class = EquipmentForm

    def get(self,request,*args,**kwargs):
        equipment = self.get_object()   
        form = self.form_class(instance=equipment)
        context = {"form":form,"equipment_id":equipment.id}
        content = render_to_string("presale/equipment-update.html",context=context,request=request)
        return JsonResponse({"content":content},status=200)
    
    def post(self,requset,*args,**kwargs):
        form = EquipmentForm(self.request.POST,instance=self.get_object())
        if form.is_valid():
            form.save()
            return JsonResponse({"message":"success"},status=200)
        return JsonResponse({"message":"fail"},status=200)

@method_decorator(csrf_exempt, name='dispatch')
class EquipmentDeleteView(DeleteView):
    queryset=Equipment.objects.all()
    def post(self,request,*args,**kwargs):
        instance = self.get_object()
        if (instance.devices.count()>0):
            return JsonResponse({"message":"not-empty"})
        else:
            instance.delete()
            return JsonResponse({"message":"success"})


class EquipmentListView(View):
    def get(self,request,*args,**kwargs):
        equipments = Equipment.objects.all()
        categories = EquipCategory.objects.exclude(parent=None)
        context = {"equipments":equipments,"categories":categories}
        content = render_to_string("presale/equipment-list.html",context=context,request=request)
        return JsonResponse({"content":content},status=200)

class EquipmentDetailView(View):
     def get(self,request,*args,**kwargs):
        equipment = Equipment.objects.get(id=self.kwargs["id"])
        data = serializers.serialize("json",[equipment,])
        return JsonResponse({"data":data},safe=False)
        
class EquipmentDeviceListView(View):
    def get(self,request,*args,**kwargs):
        equipment_id=self.kwargs["equipment_id"]
        equipment = Equipment.objects.get(id=equipment_id)
        devices= Device.objects.filter(equipment__id=equipment_id).exclude(state="sold")
        context = {"devices":devices,"equipment":equipment}
        content = render_to_string("presale/device-list.html",context=context,request=request)
        return JsonResponse({"content":content},status=200)
    
class EquipmentDeviceUpdateView(View):
    def get(self,request,*args,**kwargs):
        device_id=self.kwargs["device_id"]
        device = Device.objects.get(id=device_id)
        form = DeviceUpdateForm(instance=device)
        context = {"device":device,"form":form}
        content = render_to_string("presale/device-update.html",context=context,request=request)
        return JsonResponse({"content":content},status=200)
    def post(self,request,*args,**kwargs):
        device_id=self.kwargs["device_id"]
        device = Device.objects.get(id=device_id)
        form = DeviceUpdateForm(self.request.POST,instance=device)
        if form.is_valid():
            form.save()
            return JsonResponse({"message":"success"},status=200)
        return JsonResponse({"message":"failed"},status=200)
         
class SupplierListView(View):
    def get(self,request,*args,**kwargs):
        suppliers = Supplier.objects.all()
        context = {}
        if("name" in self.request.GET and self.request.GET.get("name")):
            name = self.request.GET.get("name")
            suppliers = suppliers.filter(name__contains=name)
            context.update({"name":name})
    
        context.update({"suppliers":suppliers})
        content = render_to_string("presale/supplier-list.html",context=context,request=request)
        return JsonResponse({"content":content},status=200)

class SupplierCreateView(View):
    def get(self,request,*args,**kwargs):
        form = SupplierForm()
        context = {"form":form}
        content = render_to_string("presale/supplier-create.html",context=context,request=request)
        return JsonResponse({"content":content},status=200)
    
    def post(self,requset,*args,**kwargs):
        form = SupplierForm(self.request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"message":"success"},status=200)
        return JsonResponse({"message":"fail"},status=200)

class SupplierUpdateView(View):
    def get(self,request,*args,**kwargs):
        supplier_id=self.kwargs["supplier_id"]
        supplier = Supplier.objects.get(id=supplier_id)
        form = SupplierForm(instance=supplier)
        context = {"form":form,"supplier":supplier}
        content = render_to_string("presale/supplier-update.html",context=context,request=request)
        return JsonResponse({"content":content},status=200)
         
    def post(self,request,*args,**kwargs):
        supplier_id=self.kwargs["supplier_id"]
        supplier = Supplier.objects.get(id=supplier_id)
        form = SupplierForm(self.request.POST,instance=supplier)
        if form.is_valid():
            form.save()
            return JsonResponse({"message":"success"},status=200)
        return JsonResponse({"message":"failed"},status=200)

@method_decorator(csrf_exempt, name='dispatch')
class SupplierDeleteView(DeleteView):
    queryset=Supplier.objects.all()
    def post(self,request,*args,**kwargs):
        instance = self.get_object()
        if (instance.device_set.count()>0):
            return JsonResponse({"message":"not-empty"})
        else:
            instance.delete()
            return JsonResponse({"message":"success"})

class EquipDeviceInboundPDFView(View):
    def get(self,request,*args,**kwargs):
        equipment = Equipment.objects.get(id=self.kwargs["equipment_id"])
        warehouse = Warehouse.objects.get(id=self.kwargs["warehouse_id"])
        amount = self.kwargs["amount"]

        today_inbound = Inbound.objects.filter(inbound_date=timezone.now().date()).count()

        print("*****************",today_inbound)
        inbound_number=f'No.{timezone.now().date()}-{today_inbound+1}'

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="入库单.pdf"'

        pdf = canvas.Canvas(response, pagesize=A4)

        pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))

        pdf.setFont('STSong-Light', 20)
        pdf.drawString(9*cm, 24.5*cm, '入库单')
        pdf.setFont('STSong-Light', 11)
        pdf.drawString(0.5*cm, 22.8*cm,  f'入库日期:  {timezone.now().date()}')
        pdf.drawString(13.5*cm, 22.8*cm, f'入库单号: {inbound_number}')
        pdf.setFont('STSong-Light', 14)
        table_data = [['设备名称', '型号', '单位', '数量','单价','金额','备注',],
                    [equipment.name, equipment.model, '台', amount,equipment.price, equipment.price*int(amount), ''],
                    ['', '', '', '','','','']]
        table = Table(table_data, colWidths=[5*cm, 3*cm, 2*cm, 2*cm,2*cm, 2*cm,4*cm], rowHeights=0.8*cm)
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
        pdf.drawString(0.5*cm, 19.2*cm, f'入库仓库:  {warehouse.name}')
        pdf.drawString(7.5*cm, 19.2*cm, f'入库人:  {request.user.real_name}')
        pdf.drawString(13.5*cm, 19.2*cm, '送货人:')


        pdf.setFillColorRGB(255,0,0)
        pdf.setFont('STSong-Light', 20)
        pdf.drawString(9*cm, 16.5*cm, '入库单')
        pdf.setFont('STSong-Light', 11)
        pdf.drawString(0.5*cm, 14.8*cm, f'入库日期:  {timezone.now().date()}')
        pdf.drawString(13.5*cm, 14.8*cm, f'入库单号: {inbound_number}')
        pdf.setFont('STSong-Light', 14)
        table_data = [['设备名称', '型号', '单位', '数量','单价','金额','备注',],
                    [equipment.name, equipment.model, '台', amount,equipment.price, equipment.price*int(amount), ''],
                    ['', '', '', '','','','']]
        table = Table(table_data, colWidths=[5*cm, 3*cm, 2*cm, 2*cm,2*cm, 2*cm,4*cm], rowHeights=0.8*cm)
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
        pdf.drawString(0.5*cm, 11.2*cm, f'入库仓库:  {warehouse.name}')
        pdf.drawString(7.5*cm, 11.2*cm, f'入库人:  {request.user.real_name}')
        pdf.drawString(13.5*cm, 11.2*cm, '送货人:')


        pdf.setFillColorRGB(0,0,255)
        pdf.setFont('STSong-Light', 20)
        pdf.drawString(9*cm, 8.5*cm, '入库单')
        pdf.setFont('STSong-Light', 11)
        pdf.drawString(0.5*cm, 6.8*cm, f'入库日期:  {timezone.now().date()}')
        pdf.drawString(13.5*cm, 6.8*cm, f'入库单号:  {inbound_number}')
        pdf.setFont('STSong-Light', 14)
        table_data = [['设备名称', '型号', '单位', '数量','单价','金额','备注',],
                    [equipment.name, equipment.model, '台', amount,equipment.price, equipment.price*int(amount), ''],
                    ['', '', '', '','','','']]
        table = Table(table_data, colWidths=[5*cm, 3*cm, 2*cm, 2*cm,2*cm, 2*cm,4*cm], rowHeights=0.8*cm)
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
        pdf.drawString(0.5*cm, 3.2*cm, f'入库仓库:  {warehouse.name}')
        pdf.drawString(7.5*cm, 3.2*cm, f'入库人:  {request.user.real_name}')
        pdf.drawString(13.5*cm, 3.2*cm, '送货人:')



        pdf.showPage()
        pdf.save()
        
        return response
        #return FileResponse(buffer, as_attachment=True, filename='example.pdf')
