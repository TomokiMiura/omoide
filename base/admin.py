from django.contrib import admin

from . import models
# Register your models here.
admin.site.register(models.CoupleMaster)
admin.site.register(models.MenMaster)
admin.site.register(models.GirlMaster)
admin.site.register(models.OmoideTran)
admin.site.register(models.TextTran)
