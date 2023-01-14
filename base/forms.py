from .models import Room
from django.forms import ModelForm
from django.contrib.auth.models import User


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']
        
    
       
class UserForm(ModelForm):
    class Meta:
        model = User  
        fields =  ['username', 'email']
         


 