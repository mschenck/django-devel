import urllib
import logging
from xmlreader import xmltodict
from upoints import point
from models import addrlatlong

map_url = "http://maps.googleapis.com/maps/api/geocode/xml?address="
dist_range = 15


def google_geo_locator(address):
    logging.debug( "google_geo_locator(\"%s\")" % address )
    if address == "":
        logging.error( "Google recursive geo_locator could not find address" )
        return ([0], [0])

    url = map_url + urllib.quote(address) + "&sensor=false"
    xmlData = urllib.urlopen(url).read()

    dataDict = xmltodict(xmlData)    
    logging.debug( "Google dataDict: \n%s" % dataDict )

    ret_code = dataDict['status'][0]
    if ret_code == "OK":
        result = dataDict['result'][0]
        geometry = result['geometry'][0]
        location = geometry['location'][0]
        coordinates = (location['lat'], location['lng'])
        return coordinates
    elif ret_code == "OVER_QUERY_LIMIT":
        logging.error( "Google api error: %s" % ret_code )
        return ([0], [0])
    else:
        logging.error( "Google api error: %s" % ret_code )
        return google_geo_locator(" ".join(address.split(" ")[1:]))

def addr2coord(address):
    logging.debug( "addr2coord(\"%s\")" % address )

    coordinates = None
    try:
        address_obj= addrlatlong.objects.get(addr=address)
        logging.debug( "addr2coord address_obj: %s" % address_obj.__dict__ )
        if address_obj.lat != '0' and address_obj.long != '0':
            coordinates = ( address_obj.lat, address_obj.long )
    except Exception, e:
        logging.error( "Caught exception processing addrlatlong.objects.get(addr=\"%s\"): %s" % ( address, e) )

    if coordinates:
        return coordinates
    
    (lat, long) = google_geo_locator(address)
    addr = addrlatlong( addr=address, lat=lat[0], long=long[0])
    addr.save()
    return (lat, long)

def closeEnough(home, test):
    logging.debug( "closeEnough(%s, %s)" % (home, test) )

    try:
        home_location =  point.Point(home[0],home[1],"US customary")
        logging.debug( "home_location = %s" % home_location )
    except Exception, e:
        logging.error( "Caught except closeEnough:home_location: %s" % e )

    try:
        test_location = point.Point(test[0], test[1], "US customary")
        logging.debug( "test_location = %s" % test_location )
    except Exception, e:
        logging.error( "Caught except closeEnough:test_location(%s, %s): %s" % (test[0], test[1], e) )

    try:
        if home_location.distance(test_location) <= dist_range:
            return True
    except:
        pass
    return False
