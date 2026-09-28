from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Complaint, Notification

admin.site.unregister(Group)


class ComplaintAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'category',
        'city',
        'priority',
        'status',
        'created_at'
    )

    list_display_links = ('id', 'user')

    list_filter = (
        'status',
        'priority',
        'category',
        'city',
        'created_at'
    )

    search_fields = (
        'user__username',
        'category',
        'description',
        'address',
        'city',
        'state',
        'zipcode'
    )

    # Only status editable from list
    list_editable = (
        'status',
    )

    ordering = ('-created_at',)

    list_per_page = 20

    readonly_fields = (
        'title',
        'user',
        'category',
        'description',
        'state',
        'city',
        'address',
        'zipcode',
        'latitude',
        'longitude',
        'priority',
        'image',
        'created_at'
    )

    fields = (
        'title',
        'user',
        'category',
        'description',
        'state',
        'city',
        'address',
        'zipcode',
        'latitude',
        'longitude',
        'priority',
        'status',
        'image',
        'created_at'
    )

    # Disable Add Complaint
    def has_add_permission(self, request):
        return False

    # Allow delete for admin
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        extra_context['total_complaints'] = Complaint.objects.count()
        extra_context['pending'] = Complaint.objects.filter(status='Pending').count()
        extra_context['in_progress'] = Complaint.objects.filter(status='In Progress').count()
        extra_context['resolved'] = Complaint.objects.filter(status='Resolved').count()
        extra_context['high_priority'] = Complaint.objects.filter(priority='High').count()

        return super().changelist_view(request, extra_context=extra_context)


    # Create notification when status changes
    def save_model(self, request, obj, form, change):

        message = None

        if change:
            old_obj = Complaint.objects.get(pk=obj.pk)

            if old_obj.status != obj.status:

                if obj.status == "In Progress":
                    message = f"Your complaint '{obj.title}' is now being processed."

                elif obj.status == "Resolved":
                    message = f"Your complaint '{obj.title}' has been resolved."

                else:
                    message = f"Your complaint '{obj.title}' status changed to {obj.status}"

        super().save_model(request, obj, form, change)

        if message:
            Notification.objects.create(
                user=obj.user,
                message=message
            )


class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'message',
        'is_read',
        'created_at'
    )

    list_filter = (
        'is_read',
        'created_at'
    )

    ordering = ('-created_at',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(Notification, NotificationAdmin)