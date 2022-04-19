from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from . import models





'''
今回は、models.pyの中で、UserModelをOverrideしてカスタマイズしてしまったので、
このAdminで表示されるレイアウト等もOveerrideして変更を加える必要がある。
以下のクラスは、DjangoのGUIレイアウトに対応している。
'''
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ()}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password_1', 'password_2'),
        }),
    )

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Profile)
admin.site.register(models.Post)
admin.site.register(models.Comment)




