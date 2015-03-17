from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(UserProfile)
admin.site.register(Course)
admin.site.register(Membership)
admin.site.register(Interests)
admin.site.register(All_Interests)