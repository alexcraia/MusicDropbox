import dropbox
from dropboxConnect.models import Client
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
    dropboxx = DropObj()
    if dropbox.client:
        drop = "MERGE"
    else:
        dropboxx.connect()
        drop = "Se connecteaza"
    dropboxx.get_account_info()
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
                state = "You're successfully logged in!"
                return redirect('/')
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
            drop.save_credentials(user)

            return redirect('/login/')
    args= {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    return render_to_response('register.html', args)
