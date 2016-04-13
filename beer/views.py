# Anything dealing with beer models is in this view such as listing beers, searching, etc.
# May include old definitions that are no longer used. Only those in the URLS file are in use.
from django.db.models import Q
from django.db.models import Avg, Count, Min, Max
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils import simplejson
from pintquest.beer.models import Beer, Beertick, Brewery, Beerrating
import datetime

# Search for beers
# Inputs the GET of the search and renders the page statically with the results.
# Need to convert to a JSON response.
def search(request):
    # Define an empty list of errors
    errors = []
    
    # Make sure the GET method is ?q=
    if 'q' in request.GET:
        q = request.GET['q']
        # If there is not search string, add a message to the errors
        if not q:
            errors.append('Enter a search term.')
        # If the search string is too long, add that message
        elif len(q) > 20:
            errors.append('Please enter at most 20 characters.')
        # If there are no errors, query the database for the beers
        else:
            beers = Beer.objects.filter(Q(name__icontains=q) | Q(brewery__name__icontains=q))
            return render_to_response('beer/search_results.html',
                {'beers': beers, 'query': q, 'request': request})
    return render_to_response('beer/search_form.html',
        {'errors': errors, 'request': request})

# Returns a JSON for the information about the beer globally
def beerinfoJSON(request, beerID):
    # Create a blank list
    result = []
    # Make sure the input (from the URL) is an integer. Raise an error if not.
    try:
        beerID = int(beerID)
    except ValueError:
        raise Http404()
    # Try to retrieve the information on the beer. If it doesn't exist, return an empty list.
    try:
        # Query for the beer object in the model
        beerinfo = Beer.objects.get(id=beerID)
        
        if request.user.is_authenticated():
            beerticks = Beertick.objects.filter(user=request.user, beer=beerID).order_by("-time")
            count = len(beerticks)
            try:
                beerRevRq = Beerrating.objects.get(beer=beerID, user=request.user)
                if count > 0:
                    lasttick = beerticks[0]
                    result = {
                        'beerid': beerinfo.id,
                        'beer': beerinfo.name,
                        'brewery': beerinfo.brewery.name,
                        'totaldrinks': beerinfo.getTotalDrinks(),
                        'dateadded': beerinfo.beer_date_added.strftime('%B %d, %Y'),
                        'beerreview': beerRevRq.review,
                        'userdrinks': count,
                        'lastdrink': lasttick.time.strftime('%B %d, %Y at %I:%M %p'),
                        }
                else:
                    result = {
                        'beerid': beerinfo.id,
                        'beer': beerinfo.name,
                        'brewery': beerinfo.brewery.name,
                        'totaldrinks': beerinfo.getTotalDrinks(),
                        'dateadded': beerinfo.beer_date_added.strftime('%B %d, %Y'),
                        'beerreview': beerRevRq.review,
                        'userdrinks': count,
                        }
            except:
                if count > 0:
                    lasttick = beerticks[0]
                    result = {
                        'beerid': beerinfo.id,
                        'beer': beerinfo.name,
                        'brewery': beerinfo.brewery.name,
                        'totaldrinks': beerinfo.getTotalDrinks(),
                        'dateadded': beerinfo.beer_date_added.strftime('%B %d, %Y'),
                        'userdrinks': count,
                        'lastdrink': lasttick.time.strftime('%B %d, %Y at %I:%M %p'),
                        }
                else:
                    result = {
                        'beerid': beerinfo.id,
                        'beer': beerinfo.name,
                        'brewery': beerinfo.brewery.name,
                        'totaldrinks': beerinfo.getTotalDrinks(),
                        'dateadded': beerinfo.beer_date_added.strftime('%B %d, %Y'),
                        'userdrinks': count,
                        }
        else:            
            # Set the list to the needed data 
            result = {
                'beerid': beerinfo.id,
                'beer': beerinfo.name,
                'brewery': beerinfo.brewery.name,
                'totaldrinks': beerinfo.getTotalDrinks(),
                'dateadded': beerinfo.beer_date_added.strftime('%B %d, %Y')
                }
    except:
        result = [0]

    # Set a variable to a JSON parsing of the 'results' list
    json = simplejson.dumps(result, sort_keys=True)

    # Return an HttpResponse of the JSON object
    return HttpResponse(json, mimetype='application/json')  

# Currently used to render the mobile beer info page
# Will be phased out in favor of the JSON result for a standard throughout all applications
def beerinfo(request, beerID):
    try:
        beerID = int(beerID)
    except ValueError:
        raise Http404()
    try:
        beerinfo = Beer.objects.get(id=beerID)
    except:
        raise Http404()

    # Retrieve all of the drinks of the beer for the user and count the objects
    beerticks = Beertick.objects.filter(user=request.user, beer=beerID).order_by("-time")
    count = len(beerticks)
    
    # Try to get the rating if it exists.
    # If the rating exists,  then render the page.  
    # If it has a drink, then also indicate the last time it was consumed.
    # Beer can have a rating/review without a drink
    try:
        beerRevRq = Beerrating.objects.get(beer=beerID, user=request.user)
        if count > 0:
            lasttick = beerticks[0]
            return render_to_response('mobile/beer/m-beerrate.html',
                {'beerinfo': beerinfo, 'beerRevRq': beerRevRq, 'totaldrinks': beerinfo.getTotalDrinks(), 'userdrinks': count, 'lastdrink': lasttick, 'request': request})
        else:
            return render_to_response('mobile/beer/m-beerrate.html',
                {'beerinfo': beerinfo, 'beerRevRq': beerRevRq, 'totaldrinks': beerinfo.getTotalDrinks(), 'userdrinks': count, 'request': request})
    except:
        if count > 0:
            lasttick = beerticks[0]
            return render_to_response('mobile/beer/m-beerrate.html',
                {'beerinfo': beerinfo, 'totaldrinks': beerinfo.getTotalDrinks(), 'userdrinks': count, 'lastdrink': lasttick, 'request': request})
        else:
            return render_to_response('mobile/beer/m-beerrate.html',
                {'beerinfo': beerinfo, 'totaldrinks': beerinfo.getTotalDrinks(), 'userdrinks': count, 'request': request})
            
# Used to rate the beer. Make sure the beer exists in the POST and in the database
def beerrate(request):
    # Make sure the user has been authenticated already
    if request.user.is_authenticated():
        # Check to see if the is a POST request
        if request.method == 'POST':            
            if request.POST.has_key('beerid'):
                beerReq = Beer.objects.get(id=request.POST['beerid'])
                if request.POST.has_key('beerreview'):
                    beerreview = request.POST['beerreview']
                    # If the beer is already reviewed, then update it based on the POST data
                    try:
                        reviewedbeer = Beerrating.objects.get(beer=beerReq, user=request.user)
                        reviewedbeer.review = beerreview
                        reviewedbeer.time = datetime.datetime.now()
                    # Else, add a new review
                    except:            
                        reviewedbeer = Beerrating(
                            beer=beerReq,
                            user=request.user,
                            review=beerreview,
                            time=datetime.datetime.now()
                        )
                    reviewedbeer.save()
                    
                    # Return JSON with the review for the beer
                    message = reviewedbeer.review
                    json = simplejson.dumps(message)
            
                    # Return an HttpResponse of the json object
                    return HttpResponse(json, mimetype='application/json')
        else:
            return HttpResponseRedirect('/m/')
    # If the user isn't authenticated, then go to the login page
    else:
        return render_to_response("mobile/users/m-login.html")
    
def beerlist(request):
    return render_to_response('beer/list_beer.html', {'request': request})

def beerlistJSON(request):
    results = []
    
    if request.method == 'GET':
        try:            
            main_beers = Beer.objects.count()
            main_breweries = Brewery.objects.count()
            main_mcbeer = Beer.objects.values('id', 'name', 'brewery__name').order_by("brewery__name", "name")
                                                
            results = {'stats':{
                'beers': main_beers,
                'breweries': main_breweries,
            },
            'allbeers':[{
                'beer': main_mcbeers['name'],
                'beerid': main_mcbeers['id'],
                'brewery': main_mcbeers['brewery__name'],
            } for main_mcbeers in main_mcbeer],
            }
        except:
            results = []
    json = simplejson.dumps(results)
    
    return HttpResponse(json, mimetype='application/json')

def userticks(request):
    if request.user.is_authenticated():        
        return render_to_response('beer/list_beerticks.html',
            {'request': request})
    else:
        return render_to_response("users/login.html")

# Return the JSON for the beers of a user
def userticksm(request):
    # Set a blank list of results
    results = []
    

    # Define the variable for pagination
    n = 1
    resultTotal = 25
    if request.GET.has_key('pageNo'):
        n = int(request.GET['pageNo'])
    if request.GET.has_key('totalResults'):
        resultTotal = int(request.GET['totalResults'])
    resultEnd = resultTotal * n
    resultStart = resultEnd - resultTotal

       
    if request.user.is_authenticated():
        # Make sure it is a GET method
        if request.method == "GET":
            beerticks = Beertick.objects.filter(user=request.user).values('pk', 'beer_id', 'beer__name', 'beer__brewery__name', 'time').order_by("-time")[resultStart:resultEnd]
            results = [{
                'drinkno': beertick['pk'],
                'beer': beertick['beer__name'],
                'beerid': beertick['beer_id'],
                'brewery': beertick['beer__brewery__name'],
                'time': beertick['time'].strftime('%b. %d, %Y at %I:%M %p'),
                 } for beertick in beerticks ]

    # Set a variable to a json parsing of the 'results' list
    json = simplejson.dumps(results)
    if request.GET.has_key('callback'):
        callback = request.GET['callback']
        json = callback + '(' + json + ');'

    # Return an HttpResponse of the json object
    return HttpResponse(json, mimetype='application/json')
    
    # Return the JSON for the beers of a user
def userstatsJSON(request):
    # Set a blank list of results
    results = []
        
    if request.user.is_authenticated():
        # Make sure it is a GET method
        if request.method == "GET":
            try:
                user_beers = Beertick.objects.filter(user=request.user).values('beer').distinct('beer').count()
                user_breweries = Beertick.objects.filter(user=request.user).values('beer__brewery').distinct('beer__brewery').count()
                user_most_common_beer = Beertick.objects.filter(user=request.user).values('beer_id', 'beer__name', 'beer__brewery__name').order_by().annotate(beer_count=Count('beer')).order_by('-beer_count')[:1].get()
                user_last_beer = Beertick.objects.filter(user=request.user).values('beer_id', 'beer__name', 'beer__brewery__name', 'time').order_by('-time')[:1].get()            

                beerticks = Beertick.objects.filter(user=request.user).values('beer', 'beer__name', 'beer_id', 'beer__brewery__name').distinct('beer').order_by('beer__brewery__name', 'beer__name')

                results = {'stats':{
                    'userbeers': user_beers,
                    'userbreweries': user_breweries,
                    'usermcbeerid': user_most_common_beer['beer_id'],
                    'usermcbeer': user_most_common_beer['beer__name'],
                    'usermcbeerbrewery': user_most_common_beer['beer__brewery__name'],
                    'usermccount': user_most_common_beer['beer_count'],
                    'userlastbeerid': user_last_beer['beer_id'],
                    'userlastbeer': user_last_beer['beer__name'],
                    'userlastbeerbrewery': user_last_beer['beer__brewery__name'],
                    'userlasttime': user_last_beer['time'].strftime('%B %d, %Y at %I:%M %p'),
                },
                'drinks':[{
                    #'drinkno': beertick.pk,
                    'beer': beertick['beer__name'],
                    'beerid': beertick['beer_id'],
                    'brewery': beertick['beer__brewery__name'],
                    #'time': beertick.time.isoformat(),
                } for beertick in beerticks ],
                }
            except:
                results = []

    # Set a variable to a json parsing of the 'results' list
    json = simplejson.dumps(results)

    # Return an HttpResponse of the json object
    return HttpResponse(json, mimetype='application/json')
    
    
def mainBeerStatsJSON(request):
    results = []
    
    if request.method == 'GET':            
        try:
            main_beers = Beer.objects.count()
            main_breweries = Brewery.objects.count()
            main_mcbeer = Beertick.objects.values('beer', 'beer__name', 'beer__brewery__name').order_by().annotate(beer_count=Count('beer')).order_by('-beer_count')[:10]
            
            results = {'stats':{
                'beers': main_beers,
                'breweries': main_breweries,
            },
            'top_beers':[{
                'beer': main_mcbeers['beer__name'],
                'beerid': main_mcbeers['beer'],
                'brewery': main_mcbeers['beer__brewery__name'],
            } for main_mcbeers in main_mcbeer],
            }
            
        except:
            results = []
    json = simplejson.dumps(results)
    if request.GET.has_key('callback'):
        callback = request.GET['callback']
        json = callback + '(' + json + ');'
    
    return HttpResponse(json, mimetype='application/json')

def lookup(request):
    # Set a blank list of results
    results = []
   
    # Make sure it is a GET method
    if request.method == "GET":
        # Check first to see if it is looking for a 'beer'
        if request.GET.has_key('beer'):
            # See if there is also a 'brewery' in the search to refine it
            if request.GET.has_key('brewery'):
                b = request.GET['brewery']
                q = request.GET['beer']
                # Set a variable to the results
                beers = Beer.objects.filter(Q(name__icontains=q) & Q(brewery__name__icontains=b)).order_by('name')
            # If there isn't a brewery, then just search the beer
            else:
                q = request.GET['beer']
                beers = Beer.objects.filter(Q(name__icontains=q)).order_by('name')
            # Set the result list
            results = [ (beer.name) for beer in beers ] 

        # If it isn't looking for a beer, then check if its looking for a brewery
        elif request.GET.has_key('brewery'):
            q = request.GET['brewery']
            breweries = Brewery.objects.filter(Q(name__icontains=q)).order_by('name')
            results = [ (brewery.name) for brewery in breweries ]
    # Set a variable to a json parsing of the 'results' list
    json = simplejson.dumps(results)

    # Return an HttpResponse of the json object
    return HttpResponse(json, mimetype='application/json')

def beerprofile(request, beerid):
    try:
        beer = Beer.objects.get(id=beerid)
        
        return render_to_response("beer/beer_profile.html", 
                                  {
                                   'request': request, 
                                   'beer': beer.name, 
                                   'brewery': beer.brewery.name,
                                   'brewery_location':beer.brewery.location,
                                   'brewery_url':beer.brewery.url
                                   })
    except:
        return render_to_response("beer/beer_profile.html")

def beertick(request):
    # Make sure the user has been authenticated already
    if request.user.is_authenticated():
        return render_to_response('beer/beertick.html', {'request': request})

    # If the user isn't authenticated, then go to the login page
    else:
        return render_to_response("users/login.html")
        
def beertickJSON(request):
    # Make sure the user has been authenticated already
    if request.user.is_authenticated():
        # Check to see if the is a POST request
        if request.method == 'POST':            
            if request.POST.has_key('beerid'):
                beerReq = Beer.objects.get(id=request.POST['beerid'])

            else:
                breweryReq, breweryWasAdded = Brewery.objects.get_or_create(
                    name=request.POST['brewerySearchField'],
                    defaults={'brewery_date_added': datetime.datetime.now(), 'addedby': request.user})
                beerReq, beerWasAdded = Beer.objects.get_or_create(
                    name=request.POST['beerSearchField'],
                    brewery=breweryReq,
                    defaults={'beer_date_added': datetime.datetime.now(), 'addedby':request.user})
                # Set a Beertick row to the beerSearchField POST, the current user, and the current time
            beertick = Beertick(
                beer=beerReq,
                user=request.user,
                time=datetime.datetime.now())

            # Save the row
            beertick.save()

            message = "You added a " + beertick.beer.brewery.name + " " + beertick.beer.name + " to your list of beers!"
            json = simplejson.dumps(message)

            # Return an HttpResponse of the json object
            return HttpResponse(json, mimetype='application/json')

        # If it isn't a POST request, then render the beertick.html page
        else:
            beers = Beer.objects.all()
            return render_to_response('mobile/m-beertick.html',
                {'request': request})

    # If the user isn't authenticated, then go to the login page
    else:
        return render_to_response("mobile/users/m-login.html")
        
def deletedrink(request):
    # Make sure the user has been authenticated already
    if request.user.is_authenticated():
        # Check to see if the is a POST request
        if request.method == 'POST':            
            if request.POST.has_key('drinkno'):
                drinkno = request.POST['drinkno']
                try:
                    drink = Beertick.objects.get(id=drinkno)
                except:
                    raise Http404()
                drink.delete()
                
                message = "Drink deleted"
                
                json = simplejson.dumps(message)
                
                return HttpResponse(json, mimetype='application/json')
    else:
        return render_to_response("mobile/users/m-login.html")