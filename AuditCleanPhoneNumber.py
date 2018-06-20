## Audit and clean phone number

import xml.etree.cElementTree as ET
import pprint
import re

## Check if the tag is contact number ('phone')

def is_phone_number(subelement):
	if (subelement.attrib['k'] == 'phone')  :
		return True

def update_number(number): 
	expected = '0123456789'
	only_digits = ''.join(x for x in number if x in expected)
	digits = list(only_digits)
  	if len(digits) >10:
  		digits = digits[-10:]
  	updated_digits = ['('] + digits[0:3]+ [') '] + digits[3:6]+ ['-']+ digits[6:10]
	updated_number = ''.join(updated_digits)
  	return updated_number

def audit_phone(element):
	# for event, element in ET.iterparse(osm_file, events=('start',)):
	if (element.tag == 'way' or element.tag == 'node'):
		for subelement in element.iter('tag'):
			if is_phone_number(subelement):
				#print(subelement.attrib)
				# subelement.attrib['v'] = update_number(subelement.attrib['v'])
				subelement.set('v',update_number(subelement.attrib['v']))
				#print(subelement.attrib)
		return element




 

