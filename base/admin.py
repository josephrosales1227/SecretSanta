from django.contrib import admin

# Register your models here.
from .models import Group, Relation

admin.site.register(Group)
admin.site.register(Relation)