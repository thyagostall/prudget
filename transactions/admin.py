from django.contrib import admin

from transactions.models import Account, Bucket, Currency


class LoggedUserModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.exclude = ('owner',)

    def get_queryset(self, request):
        query_set = super().get_queryset(request)
        return query_set.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        try:
            obj.owner = request.user
        except AttributeError:
            pass

        super().save_model(request, obj, form, change)


admin.site.register(Account, LoggedUserModelAdmin)
admin.site.register(Bucket, LoggedUserModelAdmin)
admin.site.register(Currency, LoggedUserModelAdmin)

admin.site.site_header = 'Prudget'
admin.site.site_title = 'Prudget'
admin.site.index_title = 'Prudget'
