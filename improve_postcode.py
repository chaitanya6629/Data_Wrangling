import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint


def update_postcode(postcode):
    incorrect_list = ['Weslayan Street', '88581', '75057', '7-', '73032', '74404']
    updated_postcode = postcode
    if ('TX ' in postcode):
        updated_postcode = postcode.replace('TX ', '')
    if ('tx ' in postcode):
        updated_postcode = postcode.replace('tx ', '')
    if (postcode in incorrect_list):
        return None
    return updated_postcode

def improve_postcode():
    for pin in incorrect_postcodes:
        better_postcode = update_postcode(pin)
        print pin, "=>", better_postcode


improve_postcode()