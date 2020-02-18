from django.contrib import admin
from .models import Farmer, OTPTokenPhone, ExpertApply, Expert, Others
# Register your models here.
admin.site.register(Farmer)
admin.site.register(OTPTokenPhone)
admin.site.register(ExpertApply)
admin.site.register(Expert)
admin.site.register(Others)

