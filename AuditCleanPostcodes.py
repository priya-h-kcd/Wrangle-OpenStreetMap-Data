## Audit and clean postcodes

import xml.etree.cElementTree as ET
import pprint
import re

## Check if the tag is postcode (addr:postcode)

def is_postcode(subelement):
	if (subelement.attrib['k'] == 'addr:postcode')  :
		return True

def audit_postcode(osm_file):
	for event, element in ET.iterparse(osm_file, events=('start',)):
		if (element.tag == 'way' or element.tag == 'node'):
			for subelement in element.iter('tag'):
				if is_postcode(subelement):
					if (len(subelement.attrib['v']) != 5 or subelement.attrib['v'][0] != '9'):
						# print(subelement.attrib)
					#subelement.attrib['v'] = update_name(subelement.attrib['v'], mapping)
					#print(subelement.attrib)
	return element
