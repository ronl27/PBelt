from django.shortcuts import render, redirect, HttpResponse
# will allow you to flash the error messages
from django.contrib import messages
# will import your database, in this case User
from .models import User, UserManager

# Create your views here.
#This is where you will direct the user depending on their actions in the functions in models.py

#same concept as models.py, however views.py will retrieve the information from the database(models.py) Index is first page
def index(request):
    print ('#*' * 10 + 'route to index works' + '#*' * 10)
    if "id" in request.session:
        return redirect('/success')
    return render (request, 'loginapps/index.html')

#Will try to see if the user. Success is the
def success(request):
    print ('#*' * 10 + 'route to success works' + '#*' * 10)
    if "id" not in request.session:
        return redirect('/')
    try:
        user = User.objects.get(id=request.session["id"])
    except user.DoesNotExist:
        messages.add_message(request, messages.INFO, "User not found!")
        return('/')
    return render (request, 'loginapps/success.html', {"user" : user})

#this function will communicate with the syntax in models.py.
def register(request):
    print ('#*' * 10 + 'route to register works' + '#*' * 10)
    if request.method != 'POST':
        return redirect('/')
#below else is working with def validate in models.py
    else:
        print('*' * 100)
        print('*' * 100)
        print (request.POST)
        user_valid = User.objects.validate(request.POST)
        if user_valid[0] == True:
            print('hello')
            request.session["id"] = user_valid[1].id
        return redirect ('/success')
    # else:
    #     for message in user_valid[1]:
    #         messages.add_message(request, messages.INFO, message)
    #         return redirect('/')

def login (request):
    if request.method != "POST":
        return redirect ('/')
#below else is working with def authenticate in models.py
    else:
        print ('#' * 50)
        user = User.objects.authenticate(request.POST)
        if user[0] == True:
            request.session["id"] = user[1].id
            return redirect('/success')
        else:
            messages.add_message(request, messages.INFO, user[1])
            return redirect ('/')
#create a logout button in your success.html
def logout(request):
    if "id" in request.session:
        request.session.pop("id")
    return redirect('/')
