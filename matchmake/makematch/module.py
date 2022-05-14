import random
from . import models
from . import const
# from django.shortcuts import get_object_or_404

# トーナメント作成時に指定した数分のプレイヤーを作成
def new_player_set(tournament,player_num):

    players = []
    for i in range(player_num):
        players.append(models.Player(tournament=tournament,name=f'test{i+1}'))
    
    # 不戦勝処理用のダミープレイヤーを追加
    players.append(models.Player(tournament=tournament,name='bye',dummy=True))

    return players

def set_player_drop(matches):

    for match in matches:
        
        if match.player_A_drop and not match.player_A.dummy:
            match.player_A.drop = True
            match.player_A.save()

        if match.player_B_drop and not match.player_B.dummy:
            match.player_B.drop = True
            match.player_B.save()        

# 各プレイヤーの対戦履歴取得
def get_player_match_history(players):

    # 各マッチの勝敗取得
    def get_vic_or_lose(match,A_or_B):

        opponent_id = None
        points = None

        # 不戦勝時の処理
        if match.walkover_match:
            opponent_id = const.BYE_ID
            points = const.WIN
            return opponent_id,points

        if A_or_B=='A':

            opponent_id = match.player_B.id

            if match.player_A_point > match.player_B_point:
                points = const.WIN
            elif match.player_A_point < match.player_B_point:
                points = const.LOSE
            else:
                points = const.DRAW

        if A_or_B=='B':

            opponent_id = match.player_A.id

            if match.player_B_point > match.player_A_point:
                points = const.WIN
            elif match.player_B_point < match.player_A_point:
                points = const.LOSE
            else:
                points = const.DRAW 
        
        return opponent_id,points

    match_history = {}
    
    for pl in players:

        pl_his = {'opponents_id':[],'get_points':[]}

        pl_matches_A = models.Match.objects.filter(player_A=pl)
        pl_matches_B = models.Match.objects.filter(player_B=pl)

        for match in pl_matches_A:
            opponent_id,points = get_vic_or_lose(match,'A')
            pl_his['opponents_id'].append(opponent_id)
            pl_his['get_points'].append(points)

        for match in pl_matches_B:
            opponent_id,points = get_vic_or_lose(match,'B')
            pl_his['opponents_id'].append(opponent_id)
            pl_his['get_points'].append(points)

        match_history[pl.id] = pl_his

    # 各プレイヤーの対戦履歴、及び結果を返す
    return match_history

# 対戦組み合わせ決定用の乱数設定用
def cal_rand_seed(players):
    for pl in players:
        pl.rnd = random.random()
        pl.save()

# ここができたらほぼ終わりみたいなもん！
def new_match_set(round,tournament):

    player_order = ('drop','-points','rnd')
    players = models.Player.objects.filter(tournament=tournament,dummy=False).order_by(*player_order)
    com_match = [-1]*len(players)

    match_history = get_player_match_history(players)

    # なるべく重複のない対戦組み合わせを決める
    for t in range(10):
        
        # 初回で決まらなければ、playerに乱数を設定して組み合わせ再抽選
        if t != 0:
            cal_rand_seed(players)
            players = models.Player.objects.filter(tournament=tournament,dummy=False).order_by(*player_order)
            com_match = [-1]*len(players)
        
        for i in range(len(players)-1):
                
            if i not in com_match:
                
                # i+1~len(players)-1までで重複しない対戦可能な相手を検索
                for j in range(i+1,len(players)):

                    pl = players[i]
                    op_choice = players[j]

                    # 対戦相手が決まっている相手だったら次の候補へ
                    if j in com_match:
                        continue
                    # 対戦候補がドロップしてたら次の候補へ
                    elif op_choice.drop:
                        continue
                    # pl自身がすでに対戦している相手だったら次の候補へ
                    elif op_choice.id in match_history[pl.id]['opponents_id']:
                        continue

                    else:
                        com_match[i] = j
                        com_match[j] = i
                        break
            
        # ドロップしているプレイヤーの数+Byeさんの数を算定
        drop_player = sum([1 for pl in players if pl.drop or pl.dummy])
        
        # 対戦相手が決まったプレイヤーの総数が、
        # ドロッププレイヤー＋Byeさんと当たった人(1名)以下なら、組分け確定
        if com_match.count(-1) < drop_player + 1:# ここの+1いらないけどとりあえず残しとく
            break

    matches = []        # matchの配列
    matched_player = [] # 対戦相手が確定したプレイヤー
    table = 1           # 対戦卓の番号

    # 作成した対戦組み合わせをもとに、matchを作成していく
    for ai,a_op in enumerate(com_match):
        
        # 対戦相手候補(a_op)が作成中の対戦組み合わせに入っておらず、
        # かつ、対戦相手候補が存在している場合(a_opが-1なら存在していない)
        if a_op not in matched_player and a_op != -1:

            matched_player.append(ai)
            matched_player.append(a_op)
            matches.append(models.Match(round=round,
                                table=table,
                                player_A=players[ai],
                                player_B=players[a_op]))
            
            table += 1
        
        # 不戦勝時の処理をする
        elif not players[ai].drop and a_op == -1:
            
            # Byeさんを召喚
            bye = models.Player.objects.get(tournament=tournament,dummy=True)

            # Byeさん入りのmatchを作成
            matches.append(models.Match(round=round,
                    walkover_match = True,
                    table=table,
                    player_A=players[ai],
                    player_B=bye))

            table += 1

    return matches

# オポネント・マッチ・ウィン・パーセンテージの計算
def cal_omw(pl,match_history):

    # 現ラウンドまでに対戦した対戦相手(id)を抽出
    opponents = match_history[pl.id]['opponents_id']

    # Byeさんを除く対戦相手のid
    not_bye_opps = []

    # 対戦相手別の合計勝ち数
    ops_wins = []
    
    for op_id in opponents:

        # 不戦勝は対戦相手にカウントしない
        if op_id != const.BYE_ID:
            ops_wins.append(match_history[op_id]['get_points'].count(const.WIN))
            not_bye_opps.append(op_id)

    # 各対戦相手の現在勝率
    op_win_per = []
    for op_win,op_id in zip(ops_wins,not_bye_opps):

        # 対戦相手が大会で参加したマッチ数を計算
        # get_pointsの長さ＝対戦相手で参加したマッチ数
        op_match_num = len(match_history[op_id]['get_points'])
        
        # 各対戦相手の現在勝率を計算
        # 対戦相手の勝率が33%未満だった場合、その相手は勝率33%として扱う
        if op_win/op_match_num >= 1/3:
            op_win_per.append(op_win/op_match_num)
        else:
            op_win_per.append(1/3)
    
    # 対戦相手ごとの最終勝率を対戦人数で平均し、
    # オポネント・マッチ・ウィン・パーセンテージ算定
    omw = sum(op_win_per) / len(not_bye_opps)

    return omw

# sowp:sum_opponents_win_point(勝手累点)の略
def cal_sowp(pl,match_history):

    # 現ラウンドまでに対戦した対戦相手(id)を抽出
    opponents = match_history[pl.id]['opponents_id']

    # 対戦相手別の合計勝ち数
    ops_wins = []
    
    for op_id in opponents:

        # 各プレイヤーの勝ち点合計を加える
        # Byeさんの勝ち点は加算しない(Byeさんは勝ち点０だけど)
        if op_id != const.BYE_ID:
            ops_wins.append(sum(match_history[op_id]['get_points']))


    sowp = sum(ops_wins)

    return sowp

def cal_avr_omw(pl,match_history,players_opw):

    # 現ラウンドまでに対戦した対戦相手を抽出
    opponents = match_history[pl.id]['opponents_id']
    # Byeさんを除く対戦相手のid
    not_bye_opps = []

    for op_id in opponents:

        # 不戦勝は対戦相手にカウントしない
        if op_id != const.BYE_ID:
            not_bye_opps.append(op_id)

    op_omws = [players_opw[op_id] for op_id in not_bye_opps]

    # 平均OMW%を算定
    avr_omw = sum(op_omws) / len(not_bye_opps)

    return avr_omw

# 各プレイヤーの戦績記録
def mem_players_score(tournament):

    # ダミープレイヤー以外のプレイヤーを取得
    players = models.Player.objects.filter(tournament=tournament,dummy=False)

    # 各プレイヤーの対戦履歴を取得
    match_history = get_player_match_history(players)

    # 各プレイヤーのomw記録用
    players_opw = {}

    # 各プレイヤーのomw、sowpを計算
    for pl in players:

        # それまでのラウンドで取得した勝ち点の合計をplに記録
        pl.points = sum(match_history[pl.id]['get_points'])
        omw = cal_omw(pl,match_history)
        pl.omw = omw
        players_opw[pl.id] = omw
        pl.sowp = cal_sowp(pl,match_history)
        pl.save()
    
    # omwを計算した後でなければavr_omwは計算できないのでこのタイミングで実施
    for pl in players:
        pl.avr_omw = cal_avr_omw(pl,match_history,players_opw)
        pl.save()
