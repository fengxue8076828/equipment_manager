from django.urls import reverse
from django.shortcuts import redirect
from django.http.response import JsonResponse
from django.views.generic import TemplateView,View,FormView,UpdateView,DeleteView,CreateView,ListView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import CustomedAuthenticationForm,UserForm,UserCreateForm,EquipCategoryForm,WarehouseForm
from django.contrib.auth.forms import PasswordChangeForm
from django.template.loader import render_to_string
from django.core import serializers
from .models import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class CustomedLoginView(LoginView):
     form_class=CustomedAuthenticationForm

class MainPanelView(LoginRequiredMixin,TemplateView):
    template_name="main_panel.html"

    def get_login_url(self):
        return reverse("login")
    
class MenuView(View):
    def get(self,request,*args,**kwargs):
        menu=request.user.role.modules.all()
        menu_data=serializers.serialize("json",menu)
        return JsonResponse({"menu":menu_data},status=200)
    
class UserProfileView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        form=UserForm(instance=self.request.user)
        context={"form":form}
        content=render_to_string("info/user-profile.html",context=context,request=self.request)
        return JsonResponse({"content":content},status=200)
    def post(self,request,*args,**kwargs):
        form=UserForm(request.POST,request.FILES,instance=self.request.user)
        if form.is_valid():
            form.save()
            messages.add_message(self.request,messages.SUCCESS,'更新成功！')
            return JsonResponse({"message":"success"},status=200)
        return JsonResponse({"message":"failed"},status=200)
    
class PasswordChangeView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        form=PasswordChangeForm(self.request.user)
        context={"form":form}
        content=render_to_string("info/user-password.html",context=context,request=self.request)
        return JsonResponse({"content":content},status=200)
    
    def post(self,request,*args,**kwargs):
        form = PasswordChangeForm(data=request.POST,user=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({"message":"success"},status=200)
        else:
            context={"form":form}
            content=render_to_string("info/user-password.html",context=context,request=self.request)
            return JsonResponse({"content":content},status=200)

class PasswordResetView(View):
    def get(self,request,*args,**kwargs):
        user_id=self.kwargs["id"]
        user=User.objects.get(id=user_id)
        user.set_password("123456")
        user.save()
        return JsonResponse({"message":"success"},status=200)
    
class UserCreateView(FormView):
    def get(self,request,*args,**kwargs):
        form=UserCreateForm()
        context={"form":form}
        content=render_to_string("info-manager/user-create.html",context=context,request=self.request)
        return JsonResponse({"content":content},status=200)
    
    def post(self,request,*args,**kwargs):
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            instance=form.save()
            instance.set_password("123456")
            messages.add_message(self.request,messages.SUCCESS,'更新成功！')
            instance.save()
            form=UserCreateForm()
        context={"form":form}
        content=render_to_string("info-manager/user-create.html",context=context,request=self.request)
        return JsonResponse({"content":content},status=200)
    
class UserListView(View):
    def get(self,request,*args,**kwargs):
        roles=Role.objects.all()
        if kwargs['role_id']=='-1':
            users=User.objects.all()
        else:
            users=User.objects.filter(role__id=kwargs['role_id'])
        context={"users":users,"roles":roles,"role_id":int(kwargs['role_id'])}
        content=render_to_string("info-manager/user-list.html",context=context,request=self.request)
        return JsonResponse({"content":content},status=200)
    
class UserDeleteView(View):
    def get(self,request,*args,**kwargs):
        user=User.objects.get(id=kwargs["id"])
        user.delete()
        roles=Role.objects.all()
        if kwargs['role_id']=='-1':
            users=User.objects.all()
        else:
            users=User.objects.filter(role__id=kwargs['role_id'])
        context={"users":users,"roles":roles,"selected_role":kwargs['role_id']}
        content=render_to_string("info-manager/user-list.html",context=context,request=self.request)
        return JsonResponse({"content":content},status=200)

class RoleListView(View):
    def get(self,request,*args,**kwargs):
        roles=Role.objects.all()
        parent_modules=Module.objects.filter(parent_module=None)
        child_modules=Module.objects.exclude(parent_module=None)

        current_parent_modules=Module.objects.filter(parent_module=None).filter(role__id=request.user.role.id)
        current_child_modules=Module.objects.exclude(parent_module=None).filter(role__id=request.user.role.id)

        context={"roles":roles,"parent_modules":parent_modules,"child_modules":child_modules,"current_parent_modules":current_parent_modules,"current_child_modules":current_child_modules}
        content=render_to_string("info-manager/role-list.html",context=context,request=self.request)
        return JsonResponse({"content":content},status=200)

@method_decorator(csrf_exempt, name='dispatch')
class RoleUpdateView(View):
    def post(self,request,*args,**kwargs):
        role_id=request.POST["role_id"]
        module_ids=request.POST["modules"]
        role=Role.objects.get(id=role_id)
        role.modules.clear()
        for module_id in module_ids.split(","):
            module=Module.objects.get(id=module_id)
            role.modules.add(module)
        role.save()

        roles=Role.objects.all()
        parent_modules=Module.objects.filter(parent_module=None)
        child_modules=Module.objects.exclude(parent_module=None)
        current_parent_modules=Module.objects.filter(parent_module=None).filter(role__id=role_id)
        current_child_modules=Module.objects.exclude(parent_module=None).filter(role__id=role_id)
        print("************",parent_modules)
        context={"roles":roles,"parent_modules":parent_modules,"child_modules":child_modules,"current_parent_modules":current_parent_modules,"role_id":role_id,"current_child_modules":current_child_modules}
        content=render_to_string("info-manager/role-list.html",context=context,request=self.request)
        return JsonResponse({"content":content},status=200)
    
class EquipCategoryListView(View):
    def get(self,request,*args,**kwargs):
        
        if "parent_id" not in kwargs:
            equip_categories = EquipCategory.objects.filter(parent=None)
            context = {"equip_categories":equip_categories}
            content = render_to_string("info-manager/category-list-template.html",context=context,request=request)
        else:
            parent_id=kwargs["parent_id"]
            equip_categories = EquipCategory.objects.filter(parent__id=parent_id)
            context = {"equip_categories":equip_categories}
            content = render_to_string("info-manager/category-list.html",context=context,request=request)
        return JsonResponse({"content":content},status=200)


@method_decorator(csrf_exempt, name='dispatch')
class EquipCategoryUpdateView(UpdateView):

    form_class = EquipCategoryForm
    queryset = EquipCategory.objects.all()

    def post(self,request,*args,**kwargs):
        instance = self.get_object()
        form = self.form_class(request.POST,instance=instance)

        if form.is_valid():
            form.save()
            messages.add_message(self.request,messages.SUCCESS,'更新成功！')
            return JsonResponse({"message":"success"},status=200)
        return JsonResponse({"message":"fail"},status=200)

@method_decorator(csrf_exempt, name='dispatch')
class EquipCategoryDeleteView(DeleteView):
    queryset = EquipCategory.objects.all()
    def post(self,request,*args,**kwargs):
        form = self.get_form()
        if form.is_valid():
            instance=self.get_object()
            children = EquipCategory.objects.filter(parent=instance)
            if children:
                children.delete()
            instance.delete()
            messages.add_message(self.request,messages.SUCCESS,'删除成功！')
            return JsonResponse({"message":"success"},status=200)
        return JsonResponse({"message":"fail"},status=200)
    
class EuipCategoryCreateView(CreateView):
    form_class=EquipCategoryForm
    def get(self,request,*args,**kwargs):
        form = self.form_class()
        context={"form":form}

        content=render_to_string("info-manager/category-create.html",context=context,request=self.request)
        return JsonResponse({"content":content},status=200)
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"message":"success"},status=200)
        return JsonResponse({"message":"fail"},status=200)
    
class WarehouseListView(View):       
    def get(self,request,*args,**kwargs):
        warehouses = Warehouse.objects.all()
        context = {"warehouses":warehouses}
        content = render_to_string("info-manager/warehouse-list.html",context=context,request=request)
        return JsonResponse({"content":content},status=200)
    
class WarehouseCreateView(CreateView):
    form_class=WarehouseForm
    def get(self,request,*args,**kwargs):
        form = self.form_class()
        context={"form":form}

        content=render_to_string("info-manager/warehouse-create.html",context=context,request=self.request)
        return JsonResponse({"content":content},status=200)
    
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"message":"success"},status=200)
        return JsonResponse({"message":"fail"},status=200)
    

@method_decorator(csrf_exempt, name='dispatch')
class WarehouseUpdateView(UpdateView):

    form_class = WarehouseForm
    queryset = Warehouse.objects.all()

    def post(self,request,*args,**kwargs):
        instance = self.get_object()
        form = self.form_class(request.POST,instance=instance)

        if form.is_valid():
            form.save()
            messages.add_message(self.request,messages.SUCCESS,'更新成功！')
            return JsonResponse({"message":"success"},status=200)
        return JsonResponse({"message":"fail"},status=200)
    

@method_decorator(csrf_exempt, name='dispatch')
class WarehouseDeleteView(DeleteView):
    queryset = Warehouse.objects.all()
    def post(self,request,*args,**kwargs):
        form = self.get_form()
        if form.is_valid():
            instance=self.get_object()
            instance.delete()
            messages.add_message(self.request,messages.SUCCESS,'删除成功！')
            return JsonResponse({"message":"success"},status=200)
        return JsonResponse({"message":"fail"},status=200)