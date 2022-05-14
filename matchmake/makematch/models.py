
from email.policy import default
from django.conf import settings
from django.db import models
import random

from django.forms import IntegerField



class Tournament(models.Model):
    title = models.CharField('タイトル', max_length=128)
    player_num = models.IntegerField(default=8)
    round = models.IntegerField(default=3)
    current_round = models.IntegerField(default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   verbose_name="投稿者",
                                   on_delete=models.CASCADE)
    created_at = models.DateTimeField("投稿日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)

    def __str__(self):
        return f'{self.created_by.username}_{self.title}'

class Player(models.Model):

    tournament = models.ForeignKey(Tournament,verbose_name="大会",
                                    related_name='join_player',
                                    on_delete=models.CASCADE)

    # プレイヤー基礎情報
    #id = models.IntegerField() # pk管理でもいいか？一意であれば良いし
    name = models.CharField(max_length=128)
    drop = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    omw = models.FloatField(default=0.0)
    sowp = models.IntegerField(default=0)        # 勝手累点
    avr_omw = models.FloatField(default=0.0)     # 平均OMW%  
    rnd = models.FloatField(default=random.random()) # 重複回避用乱数
    """ 
    # 対戦履歴情報
    opponents_id = []  # 対戦相手履歴
    match_his = []     # 各ラウンドで得た勝ち点
    # 順位算定基準
    points = 0         # 合計勝ち点
    omw = None         # OMW%
    sowp = None        # 勝手累点
    avr_omw = None     # 平均OMW%    
    """
    dummy = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.tournament.created_by.username}_{self.tournament.title}_{self.name}'  

class Round(models.Model):
    
    tournament = models.ForeignKey(Tournament,verbose_name="大会",
                                    related_name='tournament_round',
                                    on_delete=models.CASCADE)
    round = models.IntegerField()

    save_flag = models.BooleanField(default=False)

        # 将来的には完了時間を追加する
    def __str__(self):
        return f'{self.tournament.created_by.username}_{self.tournament.title}_{self.round}'  

class Match(models.Model):

    round = models.ForeignKey(Round,verbose_name="ラウンド",
                                on_delete=models.CASCADE)

    walkover_match = models.BooleanField(default=False)

    table = models.IntegerField(default=0)

    player_A = models.ForeignKey(Player,verbose_name="プレイヤーA",
                                    related_name='player_A',
                                    on_delete=models.CASCADE)

    player_A_point = models.IntegerField(default=0)

    player_A_drop = models.BooleanField(default=False)

    player_B = models.ForeignKey(Player,verbose_name="プレイヤーB",
                                    related_name='player_B',
                                    on_delete=models.CASCADE)

    player_B_point = models.IntegerField(default=0)

    player_B_drop = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.round.tournament.title}_{self.round.round}_{self.player_A.name}_{self.player_B.name}'  

class MatchHistory(models.Model):

    round = models.ForeignKey(Round,verbose_name="ラウンド",
                                on_delete=models.CASCADE)

    player = models.ForeignKey(Player,verbose_name="プレイヤー",
                                    related_name='player',
                                    on_delete=models.CASCADE)

    opponent = models.ForeignKey(Player,verbose_name="対戦相手",
                                    related_name='opponent',
                                    on_delete=models.CASCADE)
    
    matchpoint = models.IntegerField()

