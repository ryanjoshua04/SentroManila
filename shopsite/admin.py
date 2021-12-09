from django.contrib import admin
from .models import Item, OrderItem
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import csv
from django.http import HttpResponse

admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.site_header = "SENTRO MANILA ADMINISTRATOR SITE"
admin.site.site_title = "SENTRO MANILA"
admin.site.index_title = "Welcome to Sentro Manila Administration site!"

class Orders(admin.ModelAdmin):
    model = OrderItem

    readonly_fields = ['firstname','lastname','email_address','address','message','quantity','contact_number','order_itemid','item_name','orderdate','status']

    list_display = ('firstname','lastname','address','quantity','contact_number','item_name','orderdate','status')

    list_filter = ('status','orderdate')

    actions = ['mark_as_delivered','delete_model','download_as_csv']

    def mark_as_delivered(self,request,queryset):
        queryset.update(status = 'Delivered')
    mark_as_delivered.short_description = "Mark as Delivered"
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def get_actions(self, request):
        actions = super(Orders, self).get_actions(request)
        if request.user.username[0].upper() != 'J':
            del actions['delete_selected']
        return actions

    def delete_model(self, request, obj):
        for o in obj.all():
            o.delete()
    delete_model.short_description = 'Delete Order Record'


    def download_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=todays_order.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response
        
    download_as_csv.short_description = 'Download Selected Orders as CSV'
    
admin.site.register(Item)
admin.site.register(OrderItem, Orders)