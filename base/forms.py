from .models import Room, User
from django.forms import ModelForm



class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'avator', 'username', 'email']
