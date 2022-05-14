from multiprocessing import dummy
from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseForbidden

from makematch.forms import TournamentForm,PlayerForm,EditMatchFormSet
from makematch.models import Tournament,Player,Round,Match

from makematch.module import new_player_set,new_match_set,mem_players_score,set_player_drop

@login_required
def tournament_top(request):
    snippets = Tournament.objects.filter(created_by=request.user.id).order_by('-created_at')
    context = {"tournaments": snippets}
    return render(request, "makematch/top.html", context)

@login_required
def tournament_new(request):
    if request.method == 'POST':
        form = TournamentForm(request.POST)
        if form.is_valid():
            tournament = form.save(commit=False)
            tournament.created_by = request.user
            tournament.save()

            print(tournament.player_num)
            players = new_player_set(tournament,tournament.player_num)
            Player.objects.bulk_create(players)

            messages.add_message(request, messages.SUCCESS,
                                 "大会を作成しました。")
            return redirect(tournament_detail, tournament_id=tournament.pk)
        else:
            messages.add_message(request, messages.ERROR,
                                 "大会の作成に失敗しました。")
    else:
        form = TournamentForm()
    return render(request, "makematch/tournament_new.html", {'form': form})


@login_required
def tournament_edit(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    if tournament.created_by_id != request.user.id:
        return HttpResponseForbidden("この大会の編集は許可されていません。")

    if request.method == "POST":
        form = TournamentForm(request.POST, instance=tournament)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 "大会を更新しました。")
            return redirect('tournament_detail', tournament_id=tournament_id)
        else:
            messages.add_message(request, messages.ERROR,
                                 "大会の更新に失敗しました。")
    else:
        form = TournamentForm(instance=tournament)
    return render(request, 'makematch/tournament_edit.html', {'form': form})


@login_required
def tournament_detail(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    
    player_order = ('drop','-points','-omw','-sowp','-avr_omw')
    # 不戦勝処理用のダミープレイヤーは表示させない
    players = Player.objects.filter(tournament=tournament,dummy=False).order_by(*player_order)
    

    rounds = Round.objects.filter(tournament=tournament).order_by('-round')

    try:
        current_round_save_flag = Round.objects.get(tournament=tournament_id,
                                        round=tournament.current_round).save_flag
    except:
        current_round_save_flag = False

    return render(request, "makematch/tournament_detail.html", {
        'tournament': tournament,
        'players':players,
        'rounds':rounds,
        'current_round_save_flag':current_round_save_flag,
    })

@login_required
def player_edit(request, player_id):
    player = get_object_or_404(Player, pk=player_id)

    if player.tournament.created_by_id != request.user.id:
        return HttpResponseForbidden("このプレイヤーの編集は許可されていません。")

    if request.method == "POST":
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 "プレイヤーを更新しました。")
            return redirect('tournament_detail', tournament_id=player.tournament_id)
        else:
            messages.add_message(request, messages.ERROR,
                                 "プレイヤーの更新に失敗しました。")
    else:
        form = PlayerForm(instance=player)
    return render(request, 'makematch/player_edit.html', {'form': form})

@login_required
def round_new(request, tournament_id):

    tournament = get_object_or_404(Tournament, pk=tournament_id)
    
    current_round = Round.objects.filter(tournament=tournament_id).count()

    # ラウンド数がマックスまで行ってなかったら、新しいラウンドを作る
    if current_round < tournament.round:

        next_round = current_round+1
        tournament.current_round = next_round
        tournament.save()

        round = Round.objects.create(tournament=tournament,round=next_round)
        round.save()

        # Round1以外であれば、プレイヤー戦績を更新する
        if next_round != 1:
            mem_players_score(tournament)

        matches = new_match_set(round,tournament)
        Match.objects.bulk_create(matches)

        messages.add_message(request, messages.SUCCESS,
                                "新規ラウンドを作成しました。")
    else:
        messages.add_message(request, messages.ERROR,
                                "新規ラウンドの作成に失敗しました。")

    return redirect('tournament_detail', tournament_id=tournament_id)

@login_required
def save_players_score(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    mem_players_score(tournament)
    messages.add_message(request, messages.SUCCESS,
                                "プレイヤーの戦績を反映しました")
    return redirect('tournament_detail', tournament_id=tournament_id)


@login_required
def round_detail(request, round_id):
    round = get_object_or_404(Round, pk=round_id)
    matches = Match.objects.filter(round=round).all()

    if request.method == "POST":
        edit_formset = EditMatchFormSet(request.POST or None, 
                                queryset=matches,
                                initial=[{'player_A_point': 0,'player_B_point': 0, }]) 
                                       
        if edit_formset.is_valid():
            edit_formset.save()
            set_player_drop(matches)

            # 新規ラウンド作成判断用フラグをONに
            round.save_flag = True
            round.save()
            messages.add_message(request, messages.SUCCESS,
                                    "対戦結果の更新に成功しました")
        else:
            for ele in edit_formset:
                print(ele)
            messages.add_message(request, messages.ERROR,
                                    "対戦結果の更新に失敗しました")

    else:
         edit_formset = EditMatchFormSet(request.POST or None, queryset=matches)  
    return render(request, "makematch/round_detail.html", {
        'round': round,
        'edit_formset':edit_formset,
        'matches':matches,
    })