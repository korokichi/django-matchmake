from multiprocessing import dummy
from . import models
from . import const
# from django.shortcuts import get_object_or_404

def new_player_set(tournament,player_num):
    players = []
    for i in range(player_num):
        players.append(models.Player(tournament=tournament,name=f'test{i+1}'))
    
    players.append(models.Player(tournament=tournament,name='bye',dummy=True))

    return players

def get_player_match_history(players):

    # 各マッチの勝敗取得
    def get_vic_or_lose(match,A_or_B):

        opponent_id = None
        points = None

        # 不戦勝時の処理
        if match.walkover_match:
            opponent_id = -1
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

    return match_history

# ここができたらほぼ終わりみたいなもん！
def new_match_set(round,tournament):

    players = models.Player.objects.filter(tournament=tournament,dummy=False)
    player_order = ('drop','-points','rnd')
    players.order_by(*player_order)
    com_match = [-1]*len(players)

    match_history = get_player_match_history(players)

    for _ in range(10):
        # なるべき重複のない対戦組み合わせを決める

        com_match = [-1]*len(players)
        for i in range(len(players)-1):
                
            if i not in com_match:
                
                # i+1~len(players)-1までで重複しない対戦可能な相手を検索
                for j in range(i+1,len(players)):

                    pl = players[i]
                    op_choice = players[j]

                    # すでに対戦相手が決まっている相手だったら次の候補へ
                    if j in com_match:
                        continue
                    # 対戦候補がドロップしてたら次の候補へ
                    elif op_choice.drop:
                        continue

                    # すでに対戦している相手だったら次の候補へ
                    elif op_choice.id in match_history[pl.id]['opponents_id']:
                        continue

                    else:
                        com_match[i] = j
                        com_match[j] = i
                        break
            
        # ドロップしているプレイヤーの数を算定
        drop_player = sum([1 for pl in players if pl.drop or pl.dummy])
        
        # 対戦相手が決まったプレイヤーの総数が、
        # ドロッププレイヤー＋Byeさんと当たった人(1名)以下なら、組分け確定
        if com_match.count(-1) < drop_player + 1:
            break

    matches = []        # matchの配列
    matched_player = [] # 対戦相手が確定したプレイヤー
    table = 1           # 対戦卓の番号

    # 作成した対戦組み合わせをもとに、matchを作成していく
    for ai,a_op in enumerate(com_match):
        
        if a_op not in matched_player and a_op != -1:

            # 両方の対戦相手が存在している場合
            matched_player.append(ai)
            matched_player.append(a_op)
            matches.append(models.Match(round=round,
                                table=table,
                                player_A=players[ai],
                                player_B=players[a_op]))
            
            table += 1
        
        # 不戦勝時の処理をする
        elif not players[ai].drop and a_op == -1:
            bye = models.Player.objects.get(tournament=tournament,dummy=True)
            matches.append(models.Match(round=round,
                    walkover_match = True,
                    table=table,
                    player_A=players[ai],
                    player_B=bye))

            table += 1



    return matches
            

