from django.contrib import admin
from .models import (Institution, Class,
                     Performance)

# Register your models here.
admin.site.register(Institution)
admin.site.register(Class)
admin.site.register(Performance)
