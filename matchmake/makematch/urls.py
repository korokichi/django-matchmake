from django.urls import path

from makematch import views

urlpatterns = [
    path("new/", views.tournament_new, name="tournament_new"),
    path("<int:tournament_id>/", views.tournament_detail, name="tournament_detail"),
    path("<int:tournament_id>/edit/", views.tournament_edit, name="tournament_edit"),
    path("<int:tournament_id>/save_players_score/", views.save_players_score, name="save_players_score"),
    path("player/<int:player_id>/edit/", views.player_edit, name="player_edit"),
    path("round/<int:tournament_id>/new/", views.round_new, name="round_new"),
    path("round/<int:round_id>/", views.round_detail, name="round_detail"),
]

