from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.db.models import Sum

def index(request):
    if 'current_user' in request.session:
        return redirect ('/main')
    return render (request, 'index.html')

def login(request):
    if request.method == "POST":   
        if not User.objects.authenticate(request.POST['email'], request.POST['password']):
            messages.error(request, 'Invalid Email/Password')
            return redirect('/')
        current_user = User.objects.get(email = request.POST['email'])
        request.session['current_user'] = current_user.id
        return redirect('/main')            
    else:
        return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")

def register(request):
    if request.method =="POST":
        errors = User.objects.user_validator(request.POST)        
        if len(errors) >0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        password = request.POST['password']
        pwhash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name = request.POST["first_name"],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pwhash
        )
        request.session['current_user'] = new_user.id
        return redirect('/main')
    else:
        return redirect("/")

def main(request):
    if  'current_user' not in request.session:
        return redirect("/")
    else:
        context = {
            "user" : User.objects.get(id = request.session['current_user']),
            'runs' : Run.objects.filter(user = User.objects.get(id=request.session['current_user'])),
        }
    return render(request, 'main.html', context)

def edit(request, id):
    if request.method == "GET":
        context = {
            "user" : User.objects.get(id = id),                             
        }
        return render (request, 'edit.html', context)
    else:
        errors = User.objects.edit_validator(request.POST)  
        user = User.objects.get(id=id)      
        if len(errors) >0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/edit/{user.id}')
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.email = request.POST["email"]
        user.save()  
        return redirect(f'/edit/{user.id}')

def race(request):
    if  'current_user' not in request.session:
        return redirect("/")
    else:        
        context = {
            "user" : User.objects.get(id = request.session['current_user']),
        }
    return render(request, 'race.html', context)

def runs(request):
    if  'current_user' not in request.session:
        return redirect("/")
    else:        
        context = {
            "user" : User.objects.get(id = request.session['current_user']),
        }
    return render(request, 'runs.html', context)

def messageboard(request):
    if  'current_user' not in request.session:
        return redirect("/")
    else:        
        context = {
            "user" : User.objects.get(id = request.session['current_user']),
        }
    return render(request, 'messageboard.html', context)
def stats(request, id):
    if  'current_user' not in request.session:
        return redirect("/")
    else:
        runs = User.objects.get(id = id).run.all()
        sum = 0
        for i in runs:
            sum += i.distance
        context = {
            "user" : User.objects.get(id =id ),
            'runs': User.objects.get(id = id).run.all(),
            'total_distance' : sum,
        }
    return render(request, 'stats.html', context)

def add_run(request):
    user = User.objects.get(id= request.session['current_user'])
    hours = request.POST['hours']
    minutes = request.POST['minutes']
    total_time = hours + minutes
    run = Run.objects.create(
        user = user,
        distance = request.POST['distance'],
        time = total_time,
    )
    return redirect('/main')

