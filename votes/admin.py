from django.contrib import admin
from .models import Poll, PollNominee , Vote

# Register your models here.
admin.site.register(Poll)
admin.site.register(PollNominee)
admin.site.register(Vote)