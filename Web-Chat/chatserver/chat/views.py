from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import CreateChatRoomForm, JoinChatRoomForm, RegisterForm
from .models import ChatRoom, RoomUser, Message
import uuid

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('create_or_join_room')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def create_chat_room(request):
    if request.method == 'POST':
        form = CreateChatRoomForm(request.POST)
        if form.is_valid():
            chat_room = form.save(commit=False)
            chat_room.slug = uuid.uuid4().hex
            chat_room.save()
            RoomUser.objects.create(user=request.user, chat_room=chat_room)
            return redirect('chat_room', slug=chat_room.slug)
    else:
        form = CreateChatRoomForm()
    return render(request, 'create_chat_room.html', {'form': form})

@login_required
def join_chat_room(request):
    if request.method == 'POST':
        form = JoinChatRoomForm(request.POST)
        if form.is_valid():
            room_name = form.cleaned_data['room_name']
            chat_room = get_object_or_404(ChatRoom, name=room_name)
            if not RoomUser.objects.filter(user=request.user, chat_room=chat_room).exists():
                RoomUser.objects.create(user=request.user, chat_room=chat_room)
            return redirect('chat_room', slug=chat_room.slug)
    else:
        form = JoinChatRoomForm()
    return render(request, 'join_chat_room.html', {'form': form})

def chat_room_view(request, slug):
    chat_room = get_object_or_404(ChatRoom, slug=slug)
    messages = Message.objects.filter(chat_room=chat_room).order_by('timestamp')
    users_in_room = RoomUser.objects.filter(chat_room=chat_room)

    if request.method == 'POST':
        message_content = request.POST.get('message')
        if message_content:
            Message.objects.create(
                user=request.user,
                chat_room=chat_room,
                content=message_content
            )
            return redirect('chat_room', slug=slug)

    context = {
        'chat_room': chat_room,
        'messages': messages,
        'users_in_room': users_in_room
    }
    return render(request, 'chat_room.html', context)

@login_required
def create_or_join_room(request):
    return render(request, 'create_or_join_room.html')



def room_view(request, slug):
    chat_room = get_object_or_404(ChatRoom, slug=slug)
    messages = Message.objects.filter(chat_room=chat_room).order_by('timestamp')
    users_in_room = RoomUser.objects.filter(chat_room=chat_room)

    if request.method == "POST":
        content = request.POST.get('message')
        if content:
            Message.objects.create(
                user=request.user,
                chat_room=chat_room,
                content=content
            )
    
    return render(request, 'chat_room.html', {
        'chat_room': chat_room,
        'messages': messages,
        'users_in_room': users_in_room
    })