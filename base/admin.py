from django.contrib import admin

# Register your models here.
from .models import Address
from .models import Company
from .models import Courier
from .models import DeliveryCode
from .models import DeliveryCompany
from .models import Package
from .models import Stage
from .models import StageCode
from .models import UserAccount


admin.site.register(Address)
admin.site.register(Company)
admin.site.register(Courier)
admin.site.register(DeliveryCode)
admin.site.register(DeliveryCompany)
admin.site.register(Package)
admin.site.register(Stage)
admin.site.register(StageCode)
admin.site.register(UserAccount)
