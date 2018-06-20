import xml.etree.cElementTree as ET
import AuditCleanStreetNames
import AuditCleanPhoneNumber
import csv
import codecs
import pprint
import re
from collections import defaultdict



OSM_PATH = "seattle_washington.osm"

NODES_PATH = "nodes_sample.csv"
NODE_TAGS_PATH = "nodes_tags_sample.csv"
WAYS_PATH = "ways_sample.csv"
WAY_NODES_PATH = "ways_nodes_sample.csv"
WAY_TAGS_PATH = "ways_tags_sample.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\t\r\n]')

#SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


# ================================================== #
#               Cleaning Functions                   #
# ================================================== #
def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS, problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    node_tags = []  
    way_tags = []
    # YOUR CODE HERE
    
    if element.tag == 'node':
	    for tag in element.iter('node'):
	        for key in node_attr_fields:
	        	if key in tag.attrib:
	        		node_attribs[key] = tag.attrib[key].encode("utf-8")

	    for tag in element.iter('tag'):
	        secondry_tags = {}
	        if problem_chars.match(tag.attrib['k']):
	            pass
	            
	        elif LOWER_COLON.match(tag.attrib['k']):
	            type_key = tag.attrib['k'].split(":", 1)
	            secondry_tags['id'] = element.attrib['id'].encode("utf-8")
	            secondry_tags['key'] = type_key[1].encode("utf-8")
	            secondry_tags['value'] = tag.attrib['v'].encode("utf-8")
	            secondry_tags['type'] = type_key[0].encode("utf-8")
	            
	            node_tags.append(secondry_tags)
	        else:
	            secondry_tags['id'] = element.attrib['id'].encode("utf-8")
	            secondry_tags['key'] = tag.attrib['k'].encode("utf-8")
	            secondry_tags['value'] = tag.attrib['v'].encode("utf-8")
	            secondry_tags['type'] = default_tag_type.encode("utf-8")
	            node_tags.append(secondry_tags) 

    if element.tag == 'way':
        for tag in element.iter('way'):
            for key in way_attr_fields:
                way_attribs[key] = tag.attrib[key].encode("utf-8")
        for tag in element.iter('tag'):
            secondry_tags = {}
            if problem_chars.match(tag.attrib['k']):
                pass
            
            elif LOWER_COLON.match(tag.attrib['k']):
                type_key = tag.attrib['k'].split(":", 1)
                secondry_tags['id'] = element.attrib['id'].encode("utf-8")
                secondry_tags['key'] = type_key[1].encode("utf-8")
                secondry_tags['value'] = tag.attrib['v'].encode("utf-8")
                secondry_tags['type'] = type_key[0].encode("utf-8")
            
                way_tags.append(secondry_tags)
            else:
                secondry_tags['id'] = element.attrib['id'].encode("utf-8")
                secondry_tags['key'] = tag.attrib['k'].encode("utf-8")
                secondry_tags['value'] = tag.attrib['v'].encode("utf-8")
                secondry_tags['type'] = default_tag_type.encode("utf-8")
                way_tags.append(secondry_tags) 
        count = 0    
        for tag in element.iter('nd'):
            secondry_tags = {}
            secondry_tags['id'] = element.attrib['id'].encode("utf-8")
            secondry_tags['node_id'] = tag.attrib['ref'].encode("utf-8")
            secondry_tags['position'] = count
            count +=1
            way_nodes.append(secondry_tags) 

    
    if element.tag == 'node':
        return {'node': node_attribs, 'node_tags': node_tags}
    elif element.tag == 'way':
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': way_tags}


# ================================================== #
#               Main Function                        #
# ================================================== #

def process_map(file_in, validate):
	"""Iteratively process each XML element and write to csv(s)"""
	with open(NODES_PATH, 'wb') as nodes_file, \
    		open(NODE_TAGS_PATH, 'wb') as nodes_tags_file, \
    		open(WAYS_PATH, 'wb') as ways_file, \
        	open(WAY_NODES_PATH, 'wb') as way_nodes_file, \
        	open(WAY_TAGS_PATH, 'wb') as way_tags_file:

        	nodes_writer = csv.DictWriter(nodes_file, NODE_FIELDS)
        	node_tags_writer = csv.DictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        	ways_writer = csv.DictWriter(ways_file, WAY_FIELDS)
        	way_nodes_writer = csv.DictWriter(way_nodes_file, WAY_NODES_FIELDS)
        	way_tags_writer = csv.DictWriter(way_tags_file, WAY_TAGS_FIELDS)

        	nodes_writer.writeheader()
        	node_tags_writer.writeheader()
        	ways_writer.writeheader()
        	way_nodes_writer.writeheader()
        	way_tags_writer.writeheader()

        	# count = 0
        	for element in get_element(file_in, tags=('node', 'way')):
		    	if AuditCleanStreetNames.audit_streetname(element):
		    		updated_element = AuditCleanStreetNames.audit_streetname(element)
		    	elif AuditCleanPhoneNumber.audit_phone(element):
		    		updated_element = AuditCleanPhoneNumber.audit_phone(element)
		    	else:
		    	 	updated_element = element

		    	el = shape_element(element = updated_element)



		    	if el:
		      		if updated_element.tag == 'node':
		      			nodes_writer.writerow(el['node'])
		      			for x in range(len(el['node_tags'])):
		      				node_tags_writer.writerow(el['node_tags'][x])

		          		
		        	elif updated_element.tag == 'way':
		        		ways_writer.writerow(el['way'])
		          		for x in range(len(el['way_nodes'])):
		          			way_nodes_writer.writerow(el['way_nodes'][x])
		          		for x in range(len(el['way_tags'])):
		          			way_tags_writer.writerow(el['way_tags'][x])

if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=True)