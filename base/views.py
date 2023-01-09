from django.shortcuts import render, redirect

# Create your views here.
from .models import Room
from .forms import RoomForm
# rooms = [
#     {'id': 1, 'name': 'Lets learn python!'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Frontend developers'},
# ]


def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms, }
    return render(request, 'home.html', context)  


def room(request, pk):
    room = Room.objects.get(id=pk)
    
    context = {'room': room}
    return render(request, 'room.html', context)


def create_room(request):
    form = RoomForm()
    
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            # review = form.save(commit=False)
            return redirect('home')
            
    
    context = {'form': form}
    return render(request, 'room_form.html', context)



  