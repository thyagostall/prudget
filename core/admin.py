from django.contrib import admin

from core.models import Account, Bucket
from core.session_store import get_current_user


class LoggedUserModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.exclude = ('owner',)

    def get_queryset(self, request):
        query_set = super().get_queryset(request)
        return query_set.filter(owner=get_current_user())

    def save_model(self, request, obj, form, change):
        try:
            obj.owner = get_current_user()
        except AttributeError:
            pass

        super().save_model(request, obj, form, change)


admin.site.register(Account, LoggedUserModelAdmin)
admin.site.register(Bucket, LoggedUserModelAdmin)

admin.site.site_header = 'Prudget'
admin.site.site_title = 'Prudget'
admin.site.index_title = 'Prudget'
