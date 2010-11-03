from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django import forms

from models import zipdma, dmalist, store, SearchForm
from geolib import addr2coord, closeEnough

def index(request):
    return search_form(request)

def search_form(request):
    if request.method == 'GET':
        form = SearchForm()
        return render_to_response('geo_locator/search_form.html', { 'form': form, })

    elif request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            entered_zip = form.cleaned_data['zip_code']

            my_dma = None
            my_dma_name = None

            try:
                my_dma = zipdma.objects.get(zip=entered_zip).dma
            except:
                pass

            try:
                my_dma_name = dmalist.objects.get(dma=my_dma)
            except:
                pass

            my_coord = addr2coord(entered_zip)

            store_list = []
            try:
                store_list = store.objects.all()
            except:
                pass

            results = []
            msg = ""

            for store in store_list:
                store_addr = "%s %s, %s %s" % ( store.Address, store.City, store.State, store.Zip)
                ( store_lat, store_lng ) = addr2coord( store_addr )
                try:
                    store_dma = zipdma.objects.get(zip=store.Zip).dma
                    logging.info( "User in DMA %s" % my_dma_name )
                    if my_dma == store_dma:
                        test_coord = (store_lat, store_lng)
                        if closeEnough(my_coord, test_coord):
                            results.append( (store.StoreName, store.Address, "%s, %s %s" % (store.City, store.State, store.Zip), store.Phone) )
                except:
                   test_coord = (store_lat, store_lng)
                   if closeEnough(my_coord, test_coord):
                       results.append( (store.StoreName, store.Address, "%s, %s %s" % (store.City, store.State, store.Zip), store.Phone) )

            if len(results) == 0:
                msg = "There are no stores in your area."

            return render_to_response('geo_locator/search_results.html', { 'results': results, 'msg': msg, 'dma_name': my_dma_name})
    else:
        return search_form(request)

