
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'name' ,'hotel', 'membership', 'credit_points', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'name' , 'hotel', 'membership')
    list_filter = ('is_active', 'is_staff', 'date_joined')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'credit_points', 'membership', 'hotel')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    ordering = ('date_joined', )
admin.site.register(CustomUser, CustomUserAdmin)


# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser

# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = ('email', 'age', 'is_staff', 'is_active')
#     list_filter = ('is_staff', 'is_active')

#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('age',)}),
#         ('Permissions', {'fields': ('is_staff', 'is_active')}),
#     )

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2', 'age', 'is_staff', 'is_active'),
#         }),
#     )

 