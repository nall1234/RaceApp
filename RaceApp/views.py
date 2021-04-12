from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.db.models import Sum

def index(request):
    if 'current_user' in request.session:
        return redirect ('/main')
    return render (request, 'index.html')