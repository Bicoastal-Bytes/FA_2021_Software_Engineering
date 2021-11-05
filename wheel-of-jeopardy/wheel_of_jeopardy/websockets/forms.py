# websockets/forms.py
from django import forms

class RegisterForm(forms.Form):
    player_name = forms.CharField(label="Player Name", max_length=100)
    room_name = forms.CharField(label="Room Name", max_length=100)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'