from django.contrib import admin
from django import forms
from pintquest.beer.models import Brewery, Beertype, Beer, Beertick, Beerrating
from django.contrib.auth.models import User

class BreweryForm(forms.ModelForm):
    addedby = forms.ModelChoiceField(queryset=User.objects.order_by('username'))

    class Meta:
        model = Brewery

class BeerForm(forms.ModelForm):
    addedby = forms.ModelChoiceField(queryset=User.objects.order_by('username'))

    class Meta:
        model = Beer

class BeerratingForm(forms.ModelForm):
    beer = forms.ModelChoiceField(queryset=Beer.objects.order_by('brewery__name', 'name'))
    user = forms.ModelChoiceField(queryset=User.objects.order_by('username'))

    class Meta:
        model = Beerrating
        
class BeertickForm(forms.ModelForm):
    beer = forms.ModelChoiceField(queryset=Beer.objects.order_by('brewery__name', 'name'))
    user = forms.ModelChoiceField(queryset=User.objects.order_by('username'))

    class Meta:
        model = Beertick

class BeertickAdmin(admin.ModelAdmin):
    list_display = ('user', 'beer', 'time')
    form = BeertickForm

class BeerAdmin(admin.ModelAdmin):
    list_display = ('name', 'brewery', 'beertype', 'beer_date_added', 'beer_isverified')    
    form = BeerForm
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'beertype':
            kwargs['queryset'] = Beertype.objects.order_by('description')
        if db_field.name == 'brewery':
            kwargs['queryset'] = Brewery.objects.order_by('name')
        return super(BeerAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class BreweryAdmin(admin.ModelAdmin):
    list_display = ('name', 'brewery_date_added')
    form = BreweryForm

class BeerratingAdmin(admin.ModelAdmin):
    list_display = ('user', 'beer', 'time')
    form = BeerratingForm

class BeertypeAdmin(admin.ModelAdmin):
    ordering = ('description', )

admin.site.register(Brewery, BreweryAdmin)
admin.site.register(Beer, BeerAdmin)
admin.site.register(Beertick, BeertickAdmin)
admin.site.register(Beerrating, BeerratingAdmin)
admin.site.register(Beertype, BeertypeAdmin)