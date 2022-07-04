from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(ShowManager)
admin.site.register(Show)
admin.site.register(Salesperson)
admin.site.register(Transaction)
admin.site.register(Clerk)
# admin.site.register(Spectator)
admin.site.register(Ticket)
