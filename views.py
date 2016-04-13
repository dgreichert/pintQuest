from django import forms
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context
from django.template import RequestContext
from django.template.loader import get_template

# Define the home page to be rendered depending on whether the user is logged in or not
def home(request):    
    if request.user.is_authenticated():
        return render_to_response('main/logged_in_main.html', {'request': request})
    else:
        return render_to_response('main/logged_out_main.html')
		
def mhome(request):
    if request.user.is_authenticated():
        return render_to_response('mobile/m-logged_in_main.html')
    else:
        return render_to_response('mobile/m-logged_out_main.html')
        
def about(request):
    return render_to_response('main/about.html', {'request': request})

# Define the view for to determine whether to authenticate and login the user or not
def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
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
        csrfContext = RequestContext(request)
        return render_to_response("registration/login.html", csrfContext)

# Define the view to logout the user
def logout_view(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/")

# Define the view to register a new user
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html", {
        'form': form,
    })

	
# list of mobile User Agents
mobile_uas = [
	'w3c ','acs-','alav','alca','amoi','audi','avan','benq','bird','blac',
	'blaz','brew','cell','cldc','cmd-','dang','doco','eric','hipt','inno',
	'ipaq','java','jigs','kddi','keji','leno','lg-c','lg-d','lg-g','lge-',
	'maui','maxo','midp','mits','mmef','mobi','mot-','moto','mwbp','nec-',
	'newt','noki','oper','palm','pana','pant','phil','play','port','prox',
	'qwap','sage','sams','sany','sch-','sec-','send','seri','sgh-','shar',
	'sie-','siem','smal','smar','sony','sph-','symb','t-mo','teli','tim-',
	'tosh','tsm-','upg1','upsi','vk-v','voda','wap-','wapa','wapi','wapp',
	'wapr','webc','winw','winw','xda','xda-'
	]
 
mobile_ua_hints = [ 'SymbianOS', 'Opera Mini', 'iPhone' ]
 
 
def mobileBrowser(request):
    ''' Super simple device detection, returns True for mobile devices '''
 
    mobile_browser = False
    ua = request.META['HTTP_USER_AGENT'].lower()[0:4]
 
    if (ua in mobile_uas):
        mobile_browser = True
    else:
        for hint in mobile_ua_hints:
            if request.META['HTTP_USER_AGENT'].find(hint) > 0:
                mobile_browser = True
 
    return mobile_browser
