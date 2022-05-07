
from django.conf import settings
from django.db import models


class Tournament(models.Model):
    title = models.CharField('タイトル', max_length=128)
    round = models.IntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   verbose_name="投稿者",
                                   on_delete=models.CASCADE)
    created_at = models.DateTimeField("投稿日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)

    def __str__(self):
        return self.title

class Player(models.Model):

    tournament = models.ForeignKey(Tournament,verbose_name="大会",
                                    related_name='join_player',
                                    on_delete=models.CASCADE)

    # プレイヤー基礎情報
    #id = models.IntegerField() # pk管理でもいいか？一意であれば良いし
    name = models.CharField(max_length=128)
    drop = models.BooleanField()
    """ 
    # 対戦履歴情報
    opponents_id = []  # 対戦相手履歴
    match_his = []     # 各ラウンドで得た勝ち点
    """
    # 順位算定基準
    points = 0         # 合計勝ち点
    omw = None         # OMW%
    sowp = None        # 勝手累点
    avr_omw = None     # 平均OMW%

    # 重複回避用乱数
    rnd = 0

class Round(models.Model):
    
    tournament = models.ForeignKey(Tournament,verbose_name="大会",
                                    related_name='tournament_round',
                                    on_delete=models.CASCADE)
    round = models.IntegerField()
    # 将来的には完了時間を追加する

class Match(models.Model):

    round = models.ForeignKey(Round,verbose_name="ラウンド",
                                on_delete=models.CASCADE)
    player_A = models.ForeignKey(Player,verbose_name="プレイヤーA",
                                    related_name='player_A',
                                    on_delete=models.CASCADE)

    player_B = models.ForeignKey(Player,verbose_name="プレイヤーB",
                                    related_name='player_B',
                                    on_delete=models.CASCADE)

class MatchHistory(models.Model):
    player = models.ForeignKey(Player,verbose_name="プレイヤー",
                                    related_name='player',
                                    on_delete=models.CASCADE)
    
    round = models.ForeignKey(Round,verbose_name="ラウンド",
                                on_delete=models.CASCADE)
    
    opponent = models.ForeignKey(Player,verbose_name="対戦相手",
                                    related_name='opponent',
                                    on_delete=models.CASCADE)
    
    matchpoint = models.IntegerField()

