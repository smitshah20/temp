from django import forms
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
#from PIL import Image
#import numpy as np
#import pandas as pd
#import datetime as dt
#import seaborn as sns
#import matplotlib.pyplot as plt
from django.shortcuts import render



# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fullname = request.POST['fullname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist, Please try another Username")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('home')

        if len(username)>10:
            messages.error(request, "Username Must be under 10 characters")    

        if pass1 != pass2:
            messages.error(request, "Password didn't match!")

        myuser = User.objects.create_user(username, email, pass1)
        myuser.fullname = fullname
        myuser.save()

        messages.success(request, "Your Account has been created...")

        return redirect('signin')

    return render(request, "authentication/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            return render(request, "authentication/index.html")
            

        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')

    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('home')

def graph(request):
          
    return render(request, "authentication/graph.html")

def index(request):
    output = Image.open('D:/Ganpat_University/Sem 8/WebApp/Cohort/template/authentication/plot.png')
    #output.show() 
    return render(request, "authentication/index.html")