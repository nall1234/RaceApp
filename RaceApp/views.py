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
        user = User.objects.get(id = request.session['current_user'])
        runs = user.run.order_by('-date')[:5]
        context = {
            "user" : user,
            'runs' : runs,
        }
    return render(request, 'main.html', context)

def edit(request, id):
    if request.method == "GET":
        context = {
            "user" : User.objects.get(id = id),                             
        }
        return render (request, 'edit.html', context)
    else:
        errors = User.objects.edit_validator(request.POST, id)  
        user = User.objects.get(id=id)      
        if len(errors) >0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/edit/{user.id}')
        if request.POST['first_name'] == user.first_name or request.POST['first_name'] == "":
            pass
        else:
            user.first_name = request.POST["first_name"]

        if request.POST['last_name'] == user.last_name or request.POST['last_name'] == "":
            pass
        else:
            user.last_name = request.POST["last_name"]

        if request.POST['email'] == user.email or request.POST['email'] == "":
            pass
        else:
            user.email = request.POST["email"]
        user.save()  
        return redirect(f'/edit/{user.id}')

def add_image(request, id):
    if request.method == "GET":
        context = {
            "user" : User.objects.get(id = id),                             
        }
        return render (request, 'edit.html', context)
    else:
        user = User.objects.get(id=id)
        user.image = request.FILES["image"]
        user.save()  
        return redirect(f'/edit/{user.id}')

def race(request):
    if  'current_user' not in request.session:
        return redirect("/")
    else:  
        user = User.objects.get(id = request.session['current_user'])
        races4 = user.race.filter(week=4).all()
        race4 = races4.last() 
        races3 = user.race.filter(week=3).all()
        race3 = races3.last()      
        races2 = user.race.filter(week=2).all()
        race2 = races2.last()      
        races1 = user.race.filter(week=1).all()
        race1 = races1.last()      
        context = {
            "user" : User.objects.get(id = request.session['current_user']),
            'race4': race4,
            'race3': race3,
            'race2': race2,
            'race1': race1,
        }
    return render(request, 'race.html', context)

def runs(request):
    if  'current_user' not in request.session:
        return redirect("/")
    else: 
        user = User.objects.get(id = request.session['current_user'])
        context = {
            "user" : user,
        }
    return render(request, 'runs.html', context)

def messageboard(request):
    if  'current_user' not in request.session:
        return redirect("/")
    else:        
        context = {
            "user" : User.objects.get(id = request.session['current_user']),
            'messages': Message.objects.all(),
            'comments': Comment.objects.all(),
        }
    return render(request, 'messageboard.html', context)

def add_message(request):
    user = User.objects.get(id= request.session['current_user'])
    errors = Message.objects.message_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/messageboard')
    Message.objects.create(
        message = request.POST['message'],
        message_creator = User.objects.get(id= request.session['current_user'])
    )
    return redirect('/messageboard')


def delete_message(request, message_id):
    message = Message.objects.get(id= message_id)
    message.delete()
    return redirect('/messageboard')

def add_comment(request, id):
    errors = Comment.objects.comment_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/messageboard')
    Comment.objects.create(
        comment = request.POST['comment'],
        comment_message = Message.objects.get(id =id),
        comment_creator = User.objects.get(id=request.session['current_user'])
    )
    return redirect('/messageboard')

def delete_comment(request, comment_id):
    comment = Comment.objects.get(id= comment_id)
    comment.delete()
    return redirect('/messageboard')

def stats(request, id):
    if  'current_user' not in request.session:
        return redirect("/")
    else:
        runs = User.objects.get(id = id).run.all() 
        total_runs = runs.count()       
        total_distance = 0
        time = 0
        for i in runs:
            total_distance += i.distance
        for i in runs:
            time += i.time  
        avepace = 0
        mile_split = 0
        if total_distance == 0:
            avepace = 0 
            mile_split = 0
        else:
            mile_split = time/total_distance
            avepace = 60/mile_split 
        avedistance = 0
        if total_runs ==0:
            avedistance = 0
        else:
            avedistance = total_distance/total_runs
        
        context = {
            "user" : User.objects.get(id =id ),
            'runs': User.objects.get(id = id).run.all(),
            'total_distance' : total_distance,
            'total_time': time,
            'avepace': avepace,
            'mile_split' : mile_split,
            'avedistance': avedistance,

        }
    return render(request, 'stats.html', context)

def add_run(request):
    user = User.objects.get(id= request.session['current_user'])
    hours = float(request.POST['hours'])*60
    minutes = float(request.POST['minutes'])
    total_time = float(hours) + float(minutes)
    date = request.POST['date']
    run = Run.objects.create(
        user = user,
        distance = request.POST['distance'],
        time = total_time,
        date = date,
    )
    return redirect('/')


def add_race(request):
    user = User.objects.get(id = request.session['current_user'])
    distance = float(request.POST['distance'])
    quarter = distance * 0.25
    week = 4
    sun = 0.4
    mon = 0.6
    tues = 0
    wed = 0.5
    thur = 0.7
    fri = 0
    sat = 1.0
    for i in range (4, 0, -1):
        race = Race.objects.create(
            runner = user,
            week = i,
            distance_goal = distance,
            sunday = sun * distance,
            monday = mon * distance,
            tuesday = tues * distance,
            wednesday = wed * distance,
            thursday = thur * distance,
            friday = fri * distance,
            sat = sat * distance,
        )
        distance =  distance - quarter
    return redirect('/race')
