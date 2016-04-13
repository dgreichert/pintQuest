from django.db import models
from django.contrib.auth.models import User

# Model for the Brewery table. Self explanatory. URL is the website for the brewery.
class Brewery(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(blank=True, null=True, max_length=100)
    url = models.URLField(null=True, blank=True)
    brewery_date_added = models.DateTimeField('date published', null=True)
    addedby = models.ForeignKey(User, null=True, blank=True)
    
    def __unicode__(self):
        return self.name

# Model for the types of beers such as IPA, Lager, Belgian, etc
class Beertype(models.Model):
    description = models.CharField(max_length=50)
    def __unicode__(self):
        return self.description

# Model for the beer.
class Beer(models.Model):
    name = models.CharField(max_length=255)
    # Brewery is the foreign key to the Brewery model
    brewery = models.ForeignKey(Brewery)
    # Beertype is the foreign key to the type of beer
    beertype = models.ForeignKey(Beertype, null=True, blank=True)
    # beer_abv is the ABV percentage of the beer
    beer_abv = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # Currently not used, but isverified is used to determine if the beer was verified
    # If the beer is verified, it will be shown on public lists.
    beer_isverified = models.BooleanField()
    beer_date_added = models.DateTimeField('date published')
    addedby = models.ForeignKey(User, null=True, blank=True)
    
    def __unicode__(self):
        return u'%s %s' % (self.brewery, self.name)

    def getTotalDrinks(self):
        # Total number of drinks for this beer
        return len(Beertick.objects.filter(beer=self.id))

# This model is used to hold a "drink" or "tick" of a beer for a user. 
# Each user may have multiple drinks of a single beer, and a single beer may have multiple users
# The time for a drink must be unique (i.e., the user can't drink the same beer multiple times at that instant)
class Beertick(models.Model):
    beer = models.ForeignKey(Beer)
    user = models.ForeignKey(User)
    time = models.DateTimeField()
    # Currently not used, the amount paid for the beer
    pricepaid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # In the future, add a column to link to a location API such as Google or Foursquare
    
    def __unicode__(self):
        return u'%s %s' % (self.user, self.beer)

    class Meta:
        unique_together = (("beer", "user", "time"),)

# Currently not used, but this will be used as a rating system (1-5)
class Ratingno(models.Model):
    ratingdesc = models.CharField(max_length=15)

    def __unicode__(self):
        return self.ratingdesc

# Table for the reviews and ratings of the beer for a user. One user may review many beers, but each
# user may only have one review of that beer.
class Beerrating(models.Model):
    beer = models.ForeignKey(Beer)
    user = models.ForeignKey(User)
    review = models.TextField(null=True)
    # Currently not implemented, the 1-5 rating of the beer
    rating = models.ForeignKey(Ratingno, null=True, blank=True)    
    time = models.DateTimeField()
    # Currently not implemented. Will be used to determine if the user wants his review to be public
    ispublic = models.BooleanField()
    
    class Meta:
        unique_together = (("beer", "user"),)
