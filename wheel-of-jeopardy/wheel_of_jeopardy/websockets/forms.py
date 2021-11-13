# websockets/forms.py
from django import forms

class RegisterForm(forms.Form):
    """Form to register a player to a game"""
    player_name = forms.CharField(label="Player Name", max_length=100)
    room_name = forms.CharField(widget=forms.HiddenInput(), label="Room Name", max_length=100)

    def __init__(self, *args, **kwargs):
        """Basically here to make things look nice"""
        super(RegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class CreationForm(forms.Form):
    """Form to choose how many players """
    CHOICES = [
        ('2', 2),
        ('6', 6),
        ('12', 12),
        ('18', 18),
        ('24', 24),
        ('30', 30)
    ]

    question_count = forms.ChoiceField(label="Number of Questions", choices=CHOICES)
    player_name = forms.CharField(label="Player Name", max_length=100)
    room_name = forms.CharField(label="Room Name", max_length=100)

    def __init__(self, *args, **kwargs):
        """Basically here to make things look nice"""
        super(CreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'