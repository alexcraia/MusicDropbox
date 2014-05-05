import dropbox
from dropboxConnect.models import Client, AllMusic
from django.conf import settings
from django.shortcuts import render_to_response, redirect
from dropboxConn import DropObj
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm

APP_KEY = settings.DROPBOX_CONSUMER_KEY
APP_SECRET = settings.DROPBOX_CONSUMER_SECRET


def index(request):
    user = request.user
    dropboxx = DropObj(user.client.key_token, user.client.secret_token, user)
    drop = dropboxx.get_account_info()
    return render_to_response('index.html', {'Dropbox': drop})  

def login(request):
    state = "Please login"
    username = password = ""
    c = {}
    c.update(csrf(request))
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                allmusic = AllMusic.objects.filter(user=user)
                if allmusic:
                    return redirect('/')
                return redirect('/select_music/')
            else:
                state = "Your account is not active."
    c['state'] = state
    c['username'] = username
    return render_to_response('login.html', c)

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            drop = DropObj()
            Client.objects.create(user=user)
            url = drop.get_url_connect(user)
            return redirect(url)
    args= {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    return render_to_response('register.html', args)

def first_connect(request):
    if request.GET.get('oauth_token'):
        token = request.GET.get('oauth_token')
        client = Client.objects.get(request_key = token)
        user = client.user
        drop = DropObj()
        drop.save_credentials(user)
    return redirect('/login/')

def select_music(request):
    user = request.user
    drop = DropObj(user.client.key_token, user.client.secret_token, user)
    sounds = drop.view_all_mp3()
    return render_to_response('select_music.html', {'sounds': sounds})
