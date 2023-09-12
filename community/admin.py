from django.contrib import admin
from .models import Quote, Account, Comment, QuoteLike

# Register your models here.
admin.site.register(Quote)
admin.site.register(Account)
admin.site.register(Comment)
admin.site.register(QuoteLike)