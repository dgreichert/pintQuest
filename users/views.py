from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sessions.models import Session
from django.db.models import Avg, Count, Min, Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils import simplejson
from pintquest.users.models import *
from pintquest.beer.models import Beer, Beertick, Brewery, Beerrating

from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete

def ajaxlogin(request):
    if request.method == 'POST':
        try:
            uname = User.objects.get(email=request.POST['username'])
            uname = uname.username
        except:
            uname = request.POST['username']
        
        user = authenticate(username=uname, password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                # Set a variable to a JSON parsing of the 'results' list                
                json = simplejson.dumps({'login': '1'})  
                
                if request.POST.has_key('callback'):
                    callback = request.POST['callback']
                    json = callback + '(' + json + ');'

                # Return an HttpResponse of the JSON object
                return HttpResponse(json, mimetype='application/json')
            else:
                json = simplejson.dumps({'login': '0'})
                # Return an HttpResponse of the JSON object
                return HttpResponse(json, mimetype='application/json')
        else:
            json = simplejson.dumps({'login': '0'})

            if request.POST.has_key('callback'):
                callback = request.POST['callback']
                json = callback + '(' + json + ');'
            # Return an HttpResponse of the JSON object
            return HttpResponse(json, mimetype='application/json')
    else:
        return render_to_response("users/login_ajax.html", {'request': request})
    
def checkloggedin(request):
    if request.user.is_authenticated():    
    # Make sure it is a GET method
        if request.method == "GET":
            sessionkey = request.session.session_key
            
            session = Session.objects.get(session_key=sessionkey)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)            
            
            json = simplejson.dumps({'loggedIn': 1, 'username': user.username })
    else:
        json = simplejson.dumps({'loggedIn': 0})
        
    if request.GET.has_key('callback'):
        callback = request.GET['callback']
        json = callback + '(' + json + ');'
    return HttpResponse(json, mimetype='application/json')

# Define the view for to determine whether to authenticate and login the user or not
def login_view(request):
    if request.method == 'POST':
        try:
            uname = User.objects.get(email=request.POST['username'])
            uname = uname.username
        except:
            uname = request.POST['username']

        user = authenticate(username=uname, password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                # Success
                return HttpResponseRedirect('/')
            else:
                # Disabled account
                return HttpResponse("Not active")
        else:
            # Invalid login
            return HttpResponse("Bad UN/PW")
    else:
        return render_to_response("users/login.html", {'request': request})

# Define the view for to determine whether to authenticate and login the user or not (mobile)
def mlogin_view(request):
    if request.method == 'POST':
        try:
            uname = User.objects.get(email=request.POST['username'])
            uname = uname.username
        except:
            uname = request.POST['username']

        user = authenticate(username=uname, password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                # Success
                return HttpResponseRedirect('/m/')
            else:
                # Disabled account
                return HttpResponse("Not active")
        else:
            # Invalid login
            return HttpResponse("Bad UN/PW")
    else:
        return render_to_response("mobile/users/m-login.html", {'request': request})

def profile_page(request):
    if request.user.is_authenticated():
        return render_to_response('users/userprofile.html', {'request': request})
    else:
        return HttpResponseRedirect('/')

# Define the view to logout the user
def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/")

# Define the view to logout the user (mobile)
def mlogout_view(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/m/")

def ajaxlogout(request):
    logout(request)
    json = simplejson.dumps({'loggedIn': '0'})

    if request.POST.has_key('callback'):
        callback = request.POST['callback']
        json = callback + '(' + json + ');'

     # Return an HttpResponse of the JSON object
    return HttpResponse(json, mimetype='application/json')
    

# Define the view to register a new user
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render_to_response("users/register.html", {
        'form': form,        
    })

# Define the view to register a new user -- Use this one!
def register2(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            logout(request)
        form = SignupForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            return render_to_response("users/login.html", {'request': request})
    else:
        form = SignupForm()
    return render_to_response('users/register2.html', { 'form': form })
    
    


# Do the custom password reset forms. ******* Don't use these yet!!******
def cust_password_reset(request):
    if not request.user.is_authenticated():
        return password_reset(request, 
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            post_reset_redirect='/password_reset2/done/',
            from_email='dan@localhost.com',
            )
    else:
        return HttpResponseRedirect("/")

def cust_password_reset_done(request):
    if not request.user.is_authenticated():
        return password_reset_done(request,  
            template_name='registration/password_reset_done.html')
    else:
        return HttpResponseRedirect("/")

def cust_password_reset_confirm(request, uidb36=None, token=None):   
    if not request.user.is_authenticated():
        return password_reset_confirm(request, uidb36=uidb36, token=token,
            template_name='registration/password_reset_confirm.html',
            post_reset_redirect='reset2/done/')
    else:
        return HttpResponseRedirect("/")

def cust_password_reset_complete(request): 
    if not request.user.is_authenticated():
        return password_reset_complete(request,
            template_name='registration/password_reset_complete.html')
    else:
        return HttpResponseRedirect("/")
    


