from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.contrib.auth.decorators import login_required
import bcrypt



def index(request):
    return render(request, 'index.html')



def new_user(request):
    errors = User.objects.new_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        first_name= request.POST['first_name']
        last_name= request.POST['last_name']
        email= request.POST['email']
        password= request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)
        request.session['user_id'] = new_user.id

        return redirect(f'/profile/{new_user.id}')



def login(request):
    
    errors = User.objects.return_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    login_user_list = User.objects.filter(email=request.POST['email'])  
    logged_in_user = login_user_list[0]
    request.session['user_id'] = logged_in_user.id
    return redirect(f'/profile/{logged_in_user.id}')



def profile(request, user_id): 
    context ={
        'user' : User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'profile.html', context)



def logout(request):
    request.session.flush()
    return redirect('/')