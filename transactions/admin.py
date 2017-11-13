from django.contrib import admin

from transactions.models import Account, Bucket


class AccountAdmin(admin.ModelAdmin):
    pass


class BucketAdmin(admin.ModelAdmin):
    pass


admin.site.register(Account, AccountAdmin)
admin.site.register(Bucket, BucketAdmin)
