from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.db.models import Q
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages
# Create your views here.
from .models import Room, Topic
from .forms import RoomForm
# rooms = [
#     {'id': 1, 'name': 'Lets learn python!'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Frontend developers'},
# ]

def loginPage(request):
    
    if request.user.is_authenticated():
        return redirect('home') 
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username OR Password does not exist")
        
    context = {}
    return render(request, 'login_register.html', context)


def logoutPage(request):
    logout(request)
    return redirect('home')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    
    topic = Topic.objects.all()
    room_count = rooms.count()
    
    context = {'rooms': rooms, 'topics': topic, 'room_count': room_count}
    return render(request, 'home.html', context)  


def room(request, pk):
    room = Room.objects.get(id=pk)
    
    context = {'room': room}
    return render(request, 'room.html', context)


@login_required(login_url='/login')
def create_room(request):
    form = RoomForm()
    
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
            
    
    context = {'form': form}
    return render(request, 'room_form.html', context)


@login_required(login_url='/login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse('You are not allowed here')
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'room_form.html', context)



@login_required(login_url='/login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse('You are not allowed here')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'delete.html', {'obj': room})