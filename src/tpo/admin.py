from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Company)
admin.site.register(Profile)
admin.site.register(CompanyBatchMembership)
admin.site.register(Eligibility)
admin.site.register(Qualified)