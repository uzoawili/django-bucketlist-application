from django.contrib import admin
# from django.db.models import Count
from models import BucketList, BucketListItem


class BucketListItemAdminInLine(admin.TabularInline):
    """
    Admin definiton object for the BucketListItem model
    """
    model = BucketListItem
    fields = ('name', 'description', 'done')
    fk_name = 'bucketlist'
    extra = 0


class BucketListAdmin(admin.ModelAdmin):
    """
    Admin definiton object for the BucketList model
    """
    fieldsets = [
        (None, {
            "fields": ('name', 'description','creator'),   
        }),
    ]
    readonly_fields = ('creator',)
    search_fields = ('name',)
    list_display = ('name', 'description','creator', 'date_created', 'date_modified',)
    inlines = [BucketListItemAdminInLine,]


# registers model admin classes:
admin.site.register(BucketList, BucketListAdmin)