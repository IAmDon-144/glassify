from django.contrib import admin
from .models import Glasses,Comment,Category,Glasses2,Notice


# Register your models here.
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Notice)



@admin.register(Glasses)
class GlassesAdmin(admin.ModelAdmin):
    list_display = ['id','title','code','price']

@admin.register(Glasses2)
class GlassesAdmin(admin.ModelAdmin):
    list_display = ['id','title','code','price']