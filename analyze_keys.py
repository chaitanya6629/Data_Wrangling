import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint

OSM_FILE = "houston_texas.osm"

def tag_keys(filename):
    tag = defaultdict(int)
    for event, elem in ET.iterparse(filename):
        if (elem.tag == 'way'):
            for e in elem.iter("tag"):
                    tag[e.attrib['k']] +=1
                    # adds the unique 'k' value to the tag dictionary and increments the count if encountered again
                
    return tag

pprint.pprint(tag_keys(OSM_FILE))