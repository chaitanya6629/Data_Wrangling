import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

def update_state_name(name):
    if (name != 'TX'):
        return 'TX'
    else:
        return name

def improve_state():
    for state in incorrect_state_types:
        better_state_name = update_state_name(state)
        print state, "=>", better_state_name

improve_state()