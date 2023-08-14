from django.contrib import admin
from django.contrib.auth.models import User, Group

from Client.models import ExtendedUser

# admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(ExtendedUser)
class ClientAdmin(admin.ModelAdmin):

    list_display = (
        'username',
        'last_name',
        'first_name',
        'itnumber',
        'balance',
        'date_joined',
    )

    @admin.display(description="ИНН")
    def itnumber(self, obj):
        if not obj.ITN:
                return "Не указан"
        return obj.ITN


