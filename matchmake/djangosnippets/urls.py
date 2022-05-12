from django.contrib import admin
from django.urls import path, include

from makematch.views import tournament_top

urlpatterns = [
    path('', tournament_top, name='makematch_top'),
    path('makematch/', include('makematch.urls')),
    #path('snippets/', include('snippets.urls')),
    path("accounts/", include("accounts.urls")),
    path('admin/', admin.site.urls),
]
