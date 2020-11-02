from django.contrib import admin

from . models import *


class ExpenseAdmin(admin.ModelAdmin):
    list_display=('date','description','category','amount','username','gsttot')

class Cat_gst_Admin(admin.ModelAdmin):
    list_display=('category','gst')

admin.site.register(Expense,ExpenseAdmin)
admin.site.register(Cat_gst,Cat_gst_Admin)