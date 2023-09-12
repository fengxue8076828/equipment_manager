from typing import Any, Optional
from django.core.management.base import BaseCommand
from info_manager.models import Role, Module


class Command(BaseCommand):
    def handle(self, *args, **options):
        admin = Role.objects.create(name="系统管理员")
        operator = Role.objects.create(name="操作员")
        warehouse_manager = Role.objects.create(name="库存管理员")
        maintainer = Role.objects.create(name="维修工程师")
        accountant = Role.objects.create(name="会计师")
        saler = Role.objects.create(name="销售经理")
        manager = Role.objects.create(name="项目经理")
        trainer = Role.objects.create(name="培训师")
        info = Module.objects.create(
            name="基本信息管理",
            parent_module_id=None,
            icon="<i class='fa-solid fa-circle-info'></i>",
            link=None,
        )
        presale = Module.objects.create(
            name="售前管理",
            parent_module_id=None,
            icon="<i class='fa-solid fa-universal-access'></i>",
            link=None,
        )
        postsale = Module.objects.create(
            name="售后管理",
            parent_module_id=None,
            icon="<i class='fa-brands fa-speakap'></i>",
            link=None,
        )
        maintain = Module.objects.create(
            name="检修管理",
            parent_module_id=None,
            icon="<i class='fa-solid fa-screwdriver-wrench'></i>",
            link=None,
        )
        Module.objects.create(
            name="用户管理",
            parent_module_id=1,
            icon="<i class='fa-solid fa-user'></i>",
            link="info-manager/user-list/-1",
        )
        Module.objects.create(
            name="设备类别管理",
            parent_module_id=1,
            icon="<i class='fa-solid fa-file-lines'></i>",
            link="info-manager/category-list/",
        )
        Module.objects.create(
            name="仓库管理",
            parent_module_id=1,
            icon='<i class="fa-solid fa-warehouse"></i>',
            link="info-manager/warehouse-list/",
        )
        Module.objects.create(
            name="客户管理",
            parent_module_id=3,
            icon='<i class="fa-solid fa-face-smile"></i>',
            link="postsale/client-list/",
        )
        Module.objects.create(
            name="入库管理",
            parent_module_id=2,
            icon='<i class="fa-solid fa-cart-shopping"></i>',
            link="/presale/inbound-create/",
        )
        Module.objects.create(
            name="设备及库存管理",
            parent_module_id=2,
            icon='<i class="fa-solid fa-person-shelter"></i>',
            link="presale/equipment-list/",
        )
        Module.objects.create(
            name="出库管理",
            parent_module_id=3,
            icon='<i class="fa-sharp fa-solid fa-truck"></i>',
            link="postsale/device-forsale-list/",
        )
        Module.objects.create(
            name="出库单查询",
            parent_module_id=3,
            icon='<i class="fa-solid fa-money-check-dollar"></i>',
            link="postsale/outbound-list/",
        )
        Module.objects.create(
            name="售后设备管理",
            parent_module_id=3,
            icon='<i class="fa-solid fa-desktop"></i>',
            link="postsale/device-sold-list/",
        )
        Module.objects.create(
            name="角色管理",
            parent_module_id=1,
            icon='<i class="fa-solid fa-user-group"></i>',
            link="info-manager/role-list/",
        )
        Module.objects.create(
            name="供货商管理",
            parent_module_id=2,
            icon='<i class="fa-solid fa-box"></i>',
            link="presale/supplier-list/",
        )
        Module.objects.create(
            name="结算查询",
            parent_module_id=3,
            icon='<i class="fa-solid fa-cash-register"></i>',
            link="postsale/outbound-pay-list/",
        )
        Module.objects.create(
            name="故障设备分配",
            parent_module_id=4,
            icon='<i class="fa-sharp fa-solid fa-arrow-right"></i>',
            link="maintainance/device-list/0/",
        )
        Module.objects.create(
            name="查询检修记录",
            parent_module_id=4,
            icon='<i class="fa-solid fa-hammer"></i>',
            link="maintainance/malfunction-record-query-list/",
        )
        Module.objects.create(
            name="故障设备检修",
            parent_module_id=4,
            icon='<i class="fa-solid fa-bug"></i>',
            link="maintainance/malfunction-record-list/",
        )
        admin.modules.add(info)
        admin.modules.add(presale)
        admin.modules.add(postsale)
        admin.modules.add(maintain)

        operator.modules.add(presale)
        operator.modules.add(postsale)

        warehouse_manager.modules.add(presale)

        maintainer.modules.add(maintain)

        accountant.modules.add(postsale)

        saler.modules.add(presale)
        saler.modules.add(postsale)

        manager.modules.add(presale)

        trainer.modules.add(info)
        trainer.modules.add(presale)
        trainer.modules.add(postsale)
        trainer.modules.add(maintain)

        self.stdout.write(self.style.SUCCESS("Roles and Modules created successfully."))
