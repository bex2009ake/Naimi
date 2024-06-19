from django.contrib import admin
from app.models import *
# Register your models here.


admin.site.register(User)
admin.site.register(City)
admin.site.register(OneTimePassword)
admin.site.register(Profile)
admin.site.register(ProfileImage)
admin.site.register(ProfileVideo)
admin.site.register(Favourite)