from django import forms

from makematch.models import Tournament,Player,Round,Match

class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ('title', 'player_num', 'round')

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('name', 'drop',)

class RoundForm(forms.ModelForm):
    class Meta:
        model = Round
        fields = ('round',)

class MatchForm(forms.ModelForm):

    class Meta:
        model = Match
        fields = ('player_A_point','player_A_drop','player_B_point','player_B_drop')
        # widgets = {
        #     'player_A_point': forms.NumberInput(attrs={'class': 'form-control'}),
        #     'player_B_point': forms.NumberInput(attrs={'class': 'form-control'})
        #     # cssクラスの追加(titleにtextinputclass, textにeditableクラスが追加されるようになる)
        # }

EditMatchFormSet = forms.modelformset_factory(Match,
                                form=MatchForm,extra=0)