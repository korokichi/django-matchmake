from django.urls import path

from makematch import views

urlpatterns = [
    path('', views.top, name='makematch_top'),
    path("new/", views.tournament_new, name="tournament_new"),
    path("<int:tournament_id>/", views.tournament_detail, name="tournament_detail"),
    path("<int:tournament_id>/edit/", views.tournament_edit, name="tournament_edit"),
]

