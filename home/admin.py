from django.contrib import admin
from .models import BlogPost, Event, Donation, ShowQR

admin.site.register(BlogPost)
admin.site.register(Event)
admin.site.register(Donation)
admin.site.register(ShowQR)