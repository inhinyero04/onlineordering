from django.contrib import admin
from .models import Member, Category, BranchSetup, Item, OrderItem, Cart, Payment

admin.site.site_header = "SIDC E-Store Admin"
admin.site.site_title = "Store Admin Area"
admin.site.index_title = "SIDC E-Store Admin Area"

class MemberAdmin(admin.ModelAdmin):
    list_display = ['code_number','full_name','contact_number','email']
    search_fields = ['code_number','full_name','contact_number','email']

class ItemAdmin(admin.ModelAdmin):
    list_display = ['item_code','item_name']
    search_fields = ['item_code','item_name']


admin.site.register(Member,MemberAdmin)
admin.site.register(Category)
admin.site.register(Item, ItemAdmin)
admin.site.register(BranchSetup)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(Payment)
