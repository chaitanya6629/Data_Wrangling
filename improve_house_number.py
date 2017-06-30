import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint


house_number_re = re.compile(r'^\d+(-?\d)*$')

def update_house_number(house_number):
    street_re = re.compile(r'[a-z]{3}')
    # This regex checks if street name is present in house number field
    
    m1 = street_re.search(house_number)
    better_number = house_number
    if m1:
        #print m1.group(), "    ", house_number
        split = house_number.split(" ")
        if (split[1] != "Suite"):
            return split[0]
        else:
            better_number = house_number
    if ('Ste' in better_number):
        better_number = better_number.replace('Ste', 'Suite')

    return better_number
    


def improve_house_numbers():
    for house_number in incorrect_House_Numbers:
        better_house_number = update_house_number(house_number)
        print house_number, "=>", better_house_number

improve_house_numbers()