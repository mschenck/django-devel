from django.db import models
from django import forms

class zipdma(models.Model):
    zip = models.CharField(max_length=8,primary_key=True)
    dma = models.CharField(max_length=5)
    def __unicode__(self):
            return self.zip

class addrlatlong(models.Model):
    addr = models.CharField(max_length=512,primary_key=True)
    lat = models.CharField(max_length=32)
    long = models.CharField(max_length=32)
    def __unicode__(self):
        return "%s: %s,%s" % (self.addr,self.lat,self.long)

class dmalist(models.Model):
    dma = models.IntegerField(primary_key=True)
    dmaname = models.CharField(max_length=50)
    def __unicode__(self):
            return self.dmaname

class store(models.Model):
    sid = models.IntegerField(primary_key=True)
    Retailer = models.CharField(max_length=255)
    StoreNum = models.IntegerField()
    StoreName  = models.CharField(max_length=255)
    Phone = models.CharField(max_length=20)
    Address = models.CharField(max_length=255)
    City = models.CharField(max_length=100)
    State = models.CharField(max_length=20)
    Zip = models.CharField(max_length=10)
    ScheduledDate = models.DateField()
    OpenTime = models.CharField(max_length=10)
    CloseTime = models.CharField(max_length=10)
    enabled = models.SmallIntegerField() 
    def __unicode__(self):
            return self.StoreName

class SearchForm(forms.Form):
    zip_code = forms.CharField(max_length=10)
