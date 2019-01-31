from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import User, Recording
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    return render(request, 'musiciancredits/index.html')

def log(request):
    return render(request, 'musiciancredits/login.html')

def reg(request):
    return render(request, 'musiciancredits/register.html')

def register(request):
    f = request.POST
    valid = True
    if len(f['first_name']) < 1:
        messages.error(request, 'First name cannot be left blank.')
        valid = False
    if len(f['last_name']) < 1:
        messages.error(request, 'Last name cannot be left blank.')
        valid = False
    if not EMAIL_REGEX.match(f['email']):
        messages.error(request, 'Invalid email address.')
        valid = False
    if len(f['password']) < 8:
        messages.error(request, 'Password must be at least 8 characters.')
        valid = False

    if not f['password'] == f['password_confirmation']:
        messages.error(request, 'Password and password confirm do not match.')
        valid = False

    if not valid:
        return redirect('/reg')

    else:
        if User.objects.filter(email=f['email']).exists():
            messages.error(request, 'You have already registered. Please login.')
            return redirect('/')

        hashed_pw = bcrypt.hashpw(f['password'].encode(), bcrypt.gensalt())

        user = User()
        user.first_name=f['first_name']
        user.last_name=f['last_name']
        user.email=f['email']
        user.password = hashed_pw
        user.save()

        messages.success(request, 'Successfully registered! Please log in.')
        request.session['user_id'] = user.id
        request.session['first_name'] = user.first_name

    return redirect('/log')

def login(request):
    f = request.POST
    try:
        user = User.objects.get(email = f['email'])
        password_valid = bcrypt.checkpw(f['password'].encode(), user.password.encode())
        if password_valid:
            request.session['logged_in'] = True
            request.session['user_id'] = user.id
            request.session['first_name'] = user.first_name
            # messages.success(request, 'You logged in.')
            return redirect('/dashboard')
        else:
            messages.error(request, "Password/email did not match.")
    except User.DoesNotExist:
        messages.error(request, 'Could not find user with that email.')
    return redirect('/log')

def logout(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
    if not 'user_id' in request.session:
        return redirect('/')
    user = User.objects.get(id = request.session['user_id'])
    context = {
        'user' : User.objects.get(id=request.session['user_id']),
        'recordings': Recording.objects.order_by("-year"),
        'created_recordings': Recording.objects.filter(creator_id=request.session['user_id']),
    }
    return render(request, 'musiciancredits/dashboard.html', context)

def add_recording(request):
    return render(request, 'musiciancredits/add_recording.html')

def add(request):
    f = request.POST
    g = request.FILES
    h = request.session
    valid = True
    if len(f['artist']) < 1:
        messages.error(request, 'Artist cannot be left blank.')
        valid = False
    if len(f['album']) < 1:
        messages.error(request, 'Album cannot be left blank.')
        valid = False
    if len(f['label']) < 1:
        messages.error(request, 'Label cannot be left blank.')
        valid = False
    if len(f['year']) < 1:
        messages.error(request, 'Year cannot be left blank.')
        valid = False
    if len(f['instrument']) < 1:
        messages.error(request, 'Instrument cannot be left blank.')
        valid = False

    if not valid:
        return redirect('/add_recording')

    else:
        r = Recording()
        r.artist=f['artist']
        r.album=f['album']
        r.label=f['label']
        r.year=f['year']
        r.instrument=f['instrument']
        r.spotify=f['spotify']
        r.youtube=f['youtube']
        r.creator=User.objects.get(id=h['user_id'])

        if g:
            r.cover=g['cover']
        else:
            r.cover=''
        r.save()
        r.players.add(User.objects.get(id=h['user_id']))

        messages.success(request, 'Recording successfully added!')

    return redirect('/dashboard')

def edit_account(request, user_id):
    context = {
        'user': User.objects.get(id=user_id),
    }
    return render(request, 'musiciancredits/edit_account.html', context)

def edit(request, user_id):
    f = request.POST
    valid = True
    if len(f['first_name']) < 1:
        messages.error(request, 'First name must not be left blank.')
        valid = False
    if len(f['last_name']) < 1:
        messages.error(request, 'Last name must not be left blank.')
        valid = False
    if not EMAIL_REGEX.match(f['email']):
        messages.error(request, 'Invalid email address.')
        valid = False

    if not valid:
        return redirect('/edit_account/' + str(user_id))

    else:
        user = User.objects.get(id=request.session['user_id'])
        user.first_name=f['first_name']
        user.last_name=f['last_name']
        user.email=f['email']
        user.save()

        messages.success(request, 'Account successfully edited!')
        request.session['user_id'] = user.id
        request.session['first_name'] = user.first_name

    return redirect('/dashboard')

def edit_recording(request, recording_id):
    context = {
        'recording': Recording.objects.get(id=recording_id),
    }
    return render(request, 'musiciancredits/edit_recording.html', context)

def update(request, recording_id):
    f = request.POST
    g = request.FILES
    h = request.session
    valid = True
    if len(f['artist']) < 1:
        messages.error(request, 'Artist cannot be left blank.')
        valid = False
    if len(f['album']) < 1:
        messages.error(request, 'Album cannot be left blank.')
        valid = False
    if len(f['label']) < 1:
        messages.error(request, 'Label cannot be left blank.')
        valid = False
    if len(f['year']) < 1:
        messages.error(request, 'Year cannot be left blank.')
        valid = False
    if len(f['instrument']) < 1:
        messages.error(request, 'Instrument cannot be left blank.')
        valid = False

    if not valid:
        return redirect("/edit_recording/" + str(recording_id))

    else:
        r = Recording.objects.get(id=recording_id)
        r.artist=f['artist']
        r.album=f['album']
        r.label=f['label']
        r.year=f['year']
        r.instrument=f['instrument']
        r.spotify=f['spotify']
        r.youtube=f['youtube']
        r.creator=r.creator
        if g:
            r.cover = g['cover']
        else:
            r.cover = r.cover
        r.save()
        r.players.add(User.objects.get(id=h['user_id']))

        messages.success(request, 'Recording successfully updated!')

    return redirect('/dashboard')

def delete(request, recording_id):
    r = Recording.objects.get(id=recording_id)
    r.delete()
    return redirect('/dashboard')