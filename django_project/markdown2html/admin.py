from django.contrib import admin
from .models import Course, Note
from django.db import models
from pagedown.widgets import AdminPagedownWidget


# Register your models here.
class FooModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }


admin.site.register(Course)
admin.site.register(Note, FooModelAdmin)
