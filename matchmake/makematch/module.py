from . import models
# from django.shortcuts import get_object_or_404

def new_player_set(tournament_id,player_num):
    players = []
    for _ in range(player_num):
        players.append(models.Player(tournament=tournament_id))
    return players