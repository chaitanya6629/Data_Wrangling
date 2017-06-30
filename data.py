import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict

problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    
    if element.tag == "node" or element.tag == "way":   
        node["type"] = element.tag
        node["created"] = {}
        created = {}
        node["pos"] =[ None , None]
        pos = [None,None]
        node["address"] = {}
        address={}
        node_refs = []

        for k in element.attrib:
            # Parent Element
            if (k in CREATED):
                created[k] = element.attrib[k]
            elif (k == 'lat'):
                pos[0] = float(element.attrib[k])
            elif (k == 'lon'):
                pos[1] = float(element.attrib[k])
            elif (k in ['id','visible']):
                node[k] = element.attrib[k]
            node['pos'] = pos
            node['created'] = created
            
        for tag in element.iter("tag"):
            if not(problemchars.search(tag.attrib['k'])):
                if (tag.attrib['k'] == "addr:street"):
                    address['street'] = update_street_name(tag.attrib['v'])
                            # This will put the cleaned value of street in the address dictionary
                if (tag.attrib['k'] == "addr:city"):
                    address['city'] = update_city_name(tag.attrib['v'])
                            #print address
                            # This will put the cleaned value of city in the address dictionary
                if (tag.attrib['k'] == "addr:housenumber"):
                    address['housenumber'] = update_house_number(tag.attrib['v'])
                            # This will put the cleaned value of housenumber in the address dictionary
                if (tag.attrib['k'] == "addr:postcode"):
                    address['postcode'] = update_postcode(tag.attrib['v'])
                            # This will put the cleaned value of postcode in the address dictionary
                if (tag.attrib['k'] == "addr:state"):
                    address['state'] = update_state_name(tag.attrib['v'])
                            # This will put the cleaned value of state in the address dictionary
                if (tag.attrib['k'].find("addr") == -1):
                            # If not address
                    node[tag.attrib['k']] = tag.attrib['v']
                    
                    
        for n in element.iter("nd"):
            node_refs.append(n.attrib['ref'])

        if address:
            node['address'] = address
        if node["address"] =={}:
            node.pop("address", None)
            
        if node_refs != []:
            node["node_refs"] = node_refs
        return node
    else:
        return None
    
def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

data = {}
data = process_map(OSM_FILE, False)
