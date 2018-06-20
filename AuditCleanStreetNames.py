## Audit and clean Street Names

import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

mapping = { "St": "Street",
            "St.": "Street",
            "Rd." : "Road",
            "Ave" : "Avenue",
            "E" : "East",
            "W" : "West",
            "NE" : "Northeast",
            "Rd" : "Road",
            "avenue" : "Avenue",
            "Wy" : "Way",
            "RD" : "Road",
            "n" : "North",
            "east" : "East",
            "ROAD" : "Road",
            "southwest" : "Southwest",
            "Hwy" : "Highway",
            "Blvd": "Boulevard",
            "Pkwy" : "Parkway",
            "SOUTHWEST" : "Southwest",
            "W." : "West",
            "PL" : "Place",
            "nw" : "Northwest",
            "street" : "Street",
            "Ave." : "Avenue",
            "AVENUE" : "Avenue",
            "Pl" : "Place",
            "E." : "East",
            "Ext." : "Extension",
            "N." : "North",
            "wa" : "WA",
            "bellevue" : "Bellevue",
            "southeast" : "Southeast",
            "S" : "South",
            "W" : "West",
            "Ave" : "Avenue",
            "S-300" : "300 South",
            "AVE" : "Avenue",
            "Ct" : "Court",
            "south" : "South",
            "S." : "South",
            "FI" : "Fox Island",
            "boulevard" : "Boulevard",
            "(WA)" : "WA",
            "west" : "West",
            "NE" : "Northeast",
            "Av." : "Avenue",
            "NW" : "Northwest",
            "N" : "North",
            "Steet" : "Street",
            "Se" : "Southeast",
            "CT" : "Court",
            "SW" : "Southwest",
            "ST" : "Street",
            "Blvd." : "Boulevard",
            "WA-99" : "WA 99",
            "E.Division" : "East Division",
            "Ter" : "Terrace",
            "US-101" : "US Route 101",
            "SE" : "Southeast",
            "driveway" : "Driveway",
            "Dr." : "Drive",
            "ave" : "Avenue",
            "Rd." : "Road",
            "Hwy" : "Highway",
            "Dr" : "Drive",
            "E" : "East",
            "WA-906" : "Washington State Route 906",
            "US-2" : "U.S. Route 2",
            "av." : "Avenue",
            "Ln." : "Lane",
            "SW," : "Southwest",
            "WA-507" : "Washington State Route 507",
            "US-12" : "U.S. Route 12",
            "S.E." : "Southeast",
            "st" : "Street",
            "N.E." : "Northeast",
            "se" : "Southeast"}

## Check if the tag is street address ('street:addr')

def is_street_name(subelement):
	if (subelement.attrib['k'] == 'addr:street'):
		return True
	
## Update abbreviated street names as per mapping 

def update_name(name, mapping): 
  words = name.split()
  for i in range(len(words)):
    if words[i] in mapping:
      if words[i].lower() not in ['suite', 'ste.', 'ste']: 
        # For example, don't update 'Suite E' to 'Suite East'
        words[i] = mapping[words[i]] 
        name = " ".join(words)
  return name

def audit_streetname(element):
	# for event, element in ET.iterparse(osm_file, events=('start',)):
	if element.tag == 'way':
		for subelement in element.iter('tag'):
			if is_street_name(subelement):
				#print(subelement.attrib)
				subelement.set('v',update_name(subelement.attrib['v'], mapping))
				#subelement.attrib['v'] = update_name(subelement.attrib['v'], mapping)
				#print(subelement.attrib)
		return element



