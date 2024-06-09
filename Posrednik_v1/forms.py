from django import forms

class InputForm(forms.Form):
    liczba_dostawcow = forms.IntegerField(label='Liczba dostawców')
    liczba_odbiorcow = forms.IntegerField(label='Liczba odbiorców')
