from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    context = {
        'all_users' : User.objects.all()
    }
    return render(request, 'index.html', context)

def login(request):
    errors = User.objects.loginValidator(request.POST)

    if errors:
        for key, value in errors.items():
            messages.add_message(request, messages.INFO, value)
        return redirect("/")
    else:
        return redirect("/dashboard")

    return redirect("/")

def dashboard(request):
    if 'id' not in request.session:
        return redirect("/")
    else:
        user = User.objects.get(id=request.session['id'])
        return render(request, "dashboard.html", {'user':user})

def register(request):
    errors = User.objects.regValidator(request.POST)

    if errors:
        # loop through errors and pass into messages to display on screen
        for key, value in errors.items():
            messages.add_message(request, messages.INFO, value)
        return redirect("/")
    else:
        hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        # create the user
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hash.decode())
        # save user's id in session, automatically log in user
        request.session['id'] = user.id
        return redirect("/dashboard")
