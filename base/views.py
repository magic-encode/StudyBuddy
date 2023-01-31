from .models import User
from .models import Room
from .models import Topic
from .models import Message

from .forms import RoomForm
from .forms import UserForm
from .forms import MyUserCreationForm

from django.db.models import Q

from django.shortcuts import render
from django.shortcuts import redirect

from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404

from django.urls import reverse
from django.http import HttpResponseRedirect


def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
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

    context = {'page': page}
    return render(request, 'login_register.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)

            return redirect('update_user')
        else:
            messages.error(request, 'An error occurred during registration')

    context = {'form': form}
    return render(request, 'login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topic = Topic.objects.all()
    count_topics = topic.count()

    room_count = rooms.count()

    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms,
               'topics': topic[0:4],
               'room_count': room_count,
               'count_topics': count_topics,
               'room_messages': room_messages,
               }
    return render(request, 'home.html', context)


def profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    count_topics = topics.count()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages,
               'topics': topics, 'count_topics': count_topics, }
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def like(request, pk):
    like = get_object_or_404(Room, id=request.POST.get('like_id'))

    if like.likes.filter(id=request.user.id).exists():
        like.likes.remove(request.user)
    else:
        like.likes.add(request.user)

    return HttpResponseRedirect(reverse('room', args=[str(pk)]))


def room(request, pk, **context):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    stuff = get_object_or_404(Room, id=pk)
    total_likes = stuff.total_likes()

    likes_connected = get_object_or_404(Room, id=pk)
    liked = False
    if likes_connected.likes.filter(id=request.user.id).exists():
        liked = True
    context['post_is_liked'] = liked

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room,
               'room_messages': room_messages,
               'participants': participants,
               'total_likes': total_likes,
               'liked': liked,
               }
    return render(request, 'room.html', context)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics, }
    return render(request, 'room_form.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'delete.html', {'obj': message})


@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)

    context = {'form': form}
    return render(request, 'edit-user.html', context)


def topicPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topic = Topic.objects.filter(name__icontains=q)

    context = {'topics': topic, }
    return render(request, 'topics.html', context)


def activityPage(request):
    room_messages = Message.objects.all()

    context = {'room_messages': room_messages}
    return render(request, 'activity.html', context)
