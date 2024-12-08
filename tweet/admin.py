from django.contrib import admin
from .models import tweets , register_user
# Register your models here.
admin.site.register(tweets)
admin.site.register(register_user)
