from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    model = User
    filter_horizontal = ('user_permissions', 'groups', )

admin.site.register(User, UserAdmin)
admin.site.register(Game)
admin.site.register(OwnGame)
admin.site.register(Followship)
admin.site.register(GameLog)
admin.site.register(PublishGame)
admin.site.register(Feed)