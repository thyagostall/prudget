from django.contrib import admin

from transactions.models import Account, Bucket, Currency


admin.site.register(Account, admin.ModelAdmin)
admin.site.register(Bucket, admin.ModelAdmin)
admin.site.register(Currency, admin.ModelAdmin)
