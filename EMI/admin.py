from django.contrib import admin
from .models import EmiManager
# Register your models here.

class EMIAdmin(admin.ModelAdmin):
    list_display = ('emi_name', 'monthly_amount','duration','start_date','end_date')
    search_fields = ('emi_name',)
    list_filter = ('duration',)


admin.site.register(EmiManager, EMIAdmin)
# password/name - admin