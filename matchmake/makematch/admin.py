from django.contrib import admin
from makematch.models import Tournament,Player,Round,Match

# Register your models here.
admin.site.register(Tournament)
admin.site.register(Player)
admin.site.register(Round)
admin.site.register(Match)