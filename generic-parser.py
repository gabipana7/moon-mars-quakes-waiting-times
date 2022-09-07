from xml.etree import cElementTree as ElementTree
from urllib.request import urlopen

#
# Some generic utilities I use to parse the xml
#
#---------------------------------------------------------------------------------
# function to search an xml item for the value specified by the key
#   returns the value if the item is not found, the string 'None' is returned
#   if the value is not found.
#---------------------------------------------------------------------------------
def get_xitem_as_text(item,key):
    anItem = item.find(key,ns)
    if(anItem != None):
        return anItem.text
    else:
        return 'None'
#
#---------------------------------------------------------------------------------
#  same type of function as above, but this one also checks that the item
#     has a value provided.
#---------------------------------------------------------------------------------
def get_xitem_value_as_text(item,key,valuekey):
    anItem = item.find(key,ns)
    if(anItem == None):
        return 'None'
    else:
        value = anItem.find(valuekey,ns)
        if(value != None):
            return value.text
        else:
            return 'None'
#
#---------------------------------------------------------------------------------
def search_pdicts(key, value, list_of_dictionaries):
    return [element for element in list_of_dictionaries if element[key] == value]
#



#
# To make outputting information simple, I insure that certain values are in each dictionary,  
#   whether they are defined in the xml or not. These dictionaries set up default values,
#   but as the xml is parsed, defined key value pairs are updated.
#
#defaultPick = {'stationCode':'--','networkCode':'--','channelCode':'--',
#                         'locationCode':'--','phase':'NA','time':'NA'}
#
#defaultArrival = {'timeWeight':'NA'}
#
#defaultAmplitude = {'pickID':'NA','genericAmplitude':'NA','period':'NA',
#                  'unit':'NA', 'evaluationMode':'NA'}  

#defaultType = {'earthquake':'--', 'meteorite':'--', 'not reported':'--',
#              'crash':'--'}

#
#---------------------------------------------------------------------------------
# def getEventOrigins(xevent):
#     xorigins = xevent.findall('d:origin',ns)
#     return xorigins
#
#---------------------------------------------------------------------------------
def parse_origins(xevent):
    xorigins = xevent.findall('d:origin',ns)
    origins = []
    for xorigin in xorigins:
        anOrigin = xorigin.attrib.copy()
        anOrigin.update({
        'otime': get_xitem_value_as_text(xorigin,'d:time','d:value'),
        'latitude' : get_xitem_value_as_text(xorigin,'d:latitude','d:value'),
        'longitude' : get_xitem_value_as_text(xorigin,'d:longitude','d:value'),
        'depth' : get_xitem_value_as_text(xorigin,'d:depth','d:value'),
        'dotime' : get_xitem_value_as_text(xorigin,'d:time','d:uncertainty'),
        'dlatitude' : get_xitem_value_as_text(xorigin,'d:latitude','d:uncertainty'),
        'dlongitude' : get_xitem_value_as_text(xorigin,'d:longitude','d:uncertainty'),
        'ddepth' : get_xitem_value_as_text(xorigin,'d:depth','d:uncertainty')
        })
        #
        origins.append(anOrigin)
    #
    return origins 
#
#---------------------------------------------------------------------------------   
def parse_magnitudes(xevent):
    xmags = xevent.findall('d:magnitude',ns)
    mags = []
    for xmag in xmags:
        mdict = xmag.attrib.copy()        
        mdict.update({'mag': get_xitem_value_as_text(xmag,'d:mag','d:value')})       
        mdict.update({'magType': get_xitem_as_text(xmag,'d:type')})       
        value = get_xitem_as_text(xmag,'d:evaluationMode')
        if(value!='NA'):
            mdict.update({"evaluationMode" : value})
            
        value = get_xitem_as_text(xmag,'d:originID')
        if(value!='NA'):
            mdict.update({"originID" : value})
            
        value = get_xitem_value_as_text(xmag,'d:creationInfo', 'd:agencyID')
        if(value!='NA'):
            mdict.update({"agencyID" : value})
        #
        mags.append(mdict)
    return mags
#
#---------------------------------------------------------------------------------
def parse_picks(xev):
    xpicks = xev.findall('d:pick',ns)
    picks = []
    for pick in xpicks:
        pdict = {}
        pdict.update(pick.attrib.copy())
        
        value = get_xitem_value_as_text(pick,'d:time','d:value')
        if(value!='NA'):
            pdict.update({"time" :value})

        value = get_xitem_as_text(pick,'d:phaseHint')
        if(value!='NA'):
            pdict.update({"phase" :value})

        value = get_xitem_as_text(pick,'d:evaluationMode')
        if(value!='NA'):
            pdict.update({"evaluationMode" :value})

        pdict.update(pick.find('d:waveformID',ns).attrib)
        picks.append(pdict)
    return picks
#
#---------------------------------------------------------------------------------
def parse_arrivals(xorigin):
    xarrivals = xorigin.findall('d:arrival',ns)
    arrivals = []
    for xarr in xarrivals:
        adict = {}
        value = get_xitem_as_text(xarr,'d:pickID')
        if(value!='NA'):
            adict.update({"pickID" :value})
        value = get_xitem_as_text(xarr,'d:phase')
        if(value!='NA'):
            adict.update({"phase" :value})
        value = get_xitem_as_text(xarr,'d:azimuth')
        if(value!='NA'):
            adict.update({"azimuth" :value})
        value = get_xitem_as_text(xarr,'d:distance')
        if(value!='NA'):
            adict.update({"distance" :value})
        value = get_xitem_as_text(xarr,'d:takeoffAngle')
        if(value!='NA'):
            adict.update({"takeoffAngle" :value})
        value = get_xitem_as_text(xarr,'d:timeResidual')
        if(value!='NA'):
            adict.update({"timeResidual" :value})
        value = get_xitem_as_text(xarr,'d:timeWeight')
        if(value!='NA'):
            adict.update({"timeWeight" :value})
        arrivals.append(adict)
    return arrivals    
    
#---------------------------------------------------------------------------------
def parse_longitude(xorigin):
    xlongitude = xorigin.findall('d:longitude',ns)
    longitude = []
    for long in xlongitude:
        adict = {}
        value = get_xitem_as_text(long,'d:value')
        if (value!='NA'):
            adict.update({'value':value})
        longitude.append(adict)
    return longitude

def parse_latitude(xorigin):
    xlatitude = xorigin.findall('d:latitude',ns)
    latitude = []
    for lat in xlatitude:
        adict = {}
        value = get_xitem_as_text(lat,'d:value')
        if (value!='NA'):
            adict.update({'value':value})
        latitude.append(adict)
    return latitude




#---------------------------------------------------------------------------------
#
# 'distance', 'timeResidual', 'publicID', 'timeWeight', 'time', 
#     'networkCode', 'evaluationMode', 'stationCode', 'pickID', 
#     'azimuth', 'phase', 'channelCode', 'takeoffAngle', 'locationCode'
#
#---------------------------------------------------------------------------------
def merge_arrivals_picks(arrivals,picks):
    merged = []
    for a in arrivals:
        pid = a['pickID']
        p = search_pdicts('publicID', pid, picks)
        m = a.copy()
        if(p != None):
            m.update(p[0])
        merged.append(m)
    return merged

#---------------------------------------------------------------------------------
# Make a simple tab separated table of the picks with weights greater 
#    than minWeight
def list_arrival_time_picks(arrivalTimePicks, minWeight=0.0):
    print ('StationChannel\tphase\ttime\tdistance\tazimuth\tResidual\tWeight')
    for ap in arrivalTimePicks:
        if float(ap['timeWeight']) >= minWeight:
            try:
                s0 = ap['stationCode']+'-'+ap['networkCode']+'-'+ap['channelCode']+'-'+ap['locationCode']
                s0 += '\t'+ap['phase']+'\t'+ap['time']
                s0 += '\t'+ap['distance']+'\t'+ap['azimuth']
                s0 += '\t'+ap['timeResidual']+'\t'+ap['timeWeight']
                print (s0)
            except:
                print ('Incomplete arrival time observation.')   
#
#---------------------------------------------------------------------------------
def list_magnitudes(mags):
    print ('magType\tagencyID\tmagnitude')
    for mag in mags:
        print(mag['magType'], mag['agencyID'],mag['mag'])
#
#---------------------------------------------------------------------------------
# get the preferred origin from the eventInfo dict and the origins list
#
def get_preferred_origin(eventInfo,origins):
        preforigin = eventInfo['preferredOriginID'].lower().split("/")[-1]
        for origin in origins:
            pID = origin['publicID'].lower().split("/")[-1]
            if(pID == preforigin):
                return origin
#


# name spaces employed at USGS
# need to find a way to parse these from the file.
#

ns = {'q' : 'http://quakeml.org/xmlns/quakeml',
     'd': 'http://quakeml.org/xmlns/bed/1.2',
     'mars' : 'http://quakeml.org/xmlns/bed/1.2/mars',
     'mq' : 'http://quakeml.org/xmlns/marsquake/1.0',
     'sst' : 'http://quakeml.org/xmlns/singlestation/1.0',
     'dc' : 'http://purl.org/dc/elements/1.1/'}

def parse_usgs_xml(filepath):
    # Import xml from online:
    # url = 'http://earthquake.usgs.gov/realtime/product/phase-data/us20007z6r/us/1481210600040/quakeml.xml'
    # response = urllib2.urlopen(url)
    # xmlstring = response.read()
    # xroot = ElementTree.fromstring(xmlstring)
    # 
    # Import xml from a file
    #filepath = "20120411-OffShoreSumatra.xml"
    #
    xtree = ElementTree.parse(filepath)
    xroot = xtree.getroot()
    #
    xeventParameters = xroot.findall('d:eventParameters',ns)
    #
    for ep in xeventParameters:
        xevents = ep.findall('d:event',ns)
        print(f'Found {(len(xevents))} events.' ) 
    #    
    events = []
    #
    i = 0
    for xev in xevents:
        # build an event dictionary 
        ev = {}
        #ev['eventid'] = xev.attrib["{http://purl.org/dc/elements/1.1/}eventid"]
        ev['publicID'] = xev.attrib['publicID']
        #ev['eventsource'] = xev.attrib['{http://quakeml.org/xmlns/marsquake/1.0}eventsource']
        #ev['datasource'] = xev.attrib['{http://quakeml.org/xmlns/marsquake/1.0}datasource']
        ev['preferredOriginID'] = xev.find("d:preferredOriginID",ns).text
        #ev['preferredMagnitudeID'] = xev.find("d:preferredMagnitudeID",ns).text
        #
        mags = parse_magnitudes(xev)
        picks = parse_picks(xev)
        #amplitudes = parse_amplitudes(xev)
        #
        preforigin = ev['preferredOriginID'].lower().split("/")[-1]
        xorigins = xev.findall('d:origin',ns)
        origins = parse_origins(xev)
        pxorigin = xev[0]
        n = 0
        for xorigin in xorigins:
            anOrigin = origins[n]
            pID = anOrigin['publicID'].lower().split("/")[-1]
            if(pID == preforigin):
                pxorigin = xorigin
            n += 1
        #
        arrivals = parse_arrivals(pxorigin)
        
        # All longitude and latitudes are the same....
#        longitude = parse_longitude(pxorigin)
#        latitude = parse_latitude(pxorigin)

        # Types:
#        types = parse_types(xev)
#        descriptions = parse_descriptions(xev)
        #
        events.append({'eventInfo':ev,'magnitudes':mags,'picks':picks, 'arrivals':arrivals})
        #
        i += 1
        #
        print (f'parsed {i} events.')
        #
    return events