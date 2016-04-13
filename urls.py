from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('pintquest.views',
    # Example:
    # (r'^pintquest/', include('pintquest.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'home'),
    (r'^m/$', 'mhome'), 
    (r'^about/$', 'about'),
)

urlpatterns += patterns('pintquest.users.views',
    (r'^login/$', 'login_view'),
    (r'^m/login/$', 'mlogin_view'),
    (r'^logout/$', 'logout_view'),
    (r'^m/logout/$', 'mlogout_view'),
    #(r'^register/$', 'register'),
    (r'^register/$', 'register2'),
    (r'^login/json/$', 'ajaxlogin'),
    (r'^user/checkloggedin/$', 'checkloggedin'),
    (r'^logout/json/$', 'ajaxlogout'),
)

urlpatterns += patterns('pintquest.beer.views',
    (r'^search/$', 'search'),
    (r'^beer/drink/$', 'beertick'),
    (r'^m/drinkbeer/$', 'beertickJSON'),
    (r'^beer/lookup/$', 'lookup'),
    (r'^userlist/$', 'userticks'),
    (r'^userlist/userbeers.json$', 'userticksm'),
    (r'^user/drinks/drinks.json$', 'userticksm'),
    (r'^user/userstats.json$', 'userstatsJSON'),    
    (r'^beer/browse/$', 'beerlist'),
    (r'^beer/beers.json$', 'beerlistJSON'),
    (r'^beer/beerstats.json$', 'mainBeerStatsJSON'),
    (r'^beer/(\d+)/beerinfo.json$', 'beerinfoJSON'),
    (r'^beer/(\d+)/$', 'beerinfo'),
    (r'^beer/profile/(\d+)/$', 'beerprofile'),
    (r'^beer/rate/$', 'beerrate'),
    (r'^drink/delete/$', 'deletedrink'),
)

urlpatterns += patterns('',
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    (r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^reset/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    url(r'', include('social_auth.urls')),
)
