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
    # print("request.scheme",request.scheme)
    # print("request.body",request.body)
    # print("request.path", request.path)
    # print("request.COOKIES", request.COOKIES)
    # print("request.POST", request.POST)
    # print("request.session", request.session)
    # for key, value in request.session.items():
    #     print(f"'{key}': {value}")
    #
    # print("request.get_host()", request.get_host())
    result = User.objects.loginValidator(request.POST)

    if result[0]:
        for key, value in result[0].items():
            messages.add_message(request, messages.INFO, value, extra_tags=key)
        return redirect("/")
    else:
        request.session['id'] = result[1].id
        response = redirect("/dashboard")
        return response

    return redirect("/")

def dashboard(request):
    if 'id' not in request.session:
        return redirect("/")
    else:
        user = User.objects.get(id=request.session['id'])
        response = render(request, "dashboard.html", {'user':user})
        print(response)
        # for key, value in response.items():
        #     print(key, value)
        return response

def register(request):
    errors = User.objects.regValidator(request.POST)

    if errors:
        # loop through errors and pass into messages to display on screen
        for key, value in errors.items():
            messages.add_message(request, messages.INFO, value, extra_tags=key)
        return redirect("/")
    else:
        hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        # create the user
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hash.decode())
        # save user's id in session, automatically log in user
        request.session['id'] = user.id
        return redirect("/dashboard")
