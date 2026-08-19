from django.contrib import admin
from .models import Tag, Quote

# Register your models here.

admin.site.register(Quote)
admin.site.register(Tag)
