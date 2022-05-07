from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseForbidden

from makematch.forms import TournamentForm
from makematch.models import Tournament


def top(request):
    snippets = Tournament.objects.all()
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
    # comments = Comment.objects.filter(commented_to=tournament_id).all()
    # comment_form = CommentForm()

    return render(request, "makematch/tournament_detail.html", {
        'tournament': tournament,
    })