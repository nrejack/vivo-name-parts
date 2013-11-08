#!/user/bin/env/python
"""
    name-parts.py -- provide name parts to people in VIVO

    GIven a csv of people without name parts where for each person we have
    their URI and a display name, parse the display name into name parts
    and generate the RDF needed to add those name parts to VIVO

    Version 0.1 MC 02/21/2013
    --  Given a simple VIVO spreadsheet with one ufid display name per row,
        Use five case logic to update the name parts in VIVO
"""

__author__      = "Michael Conlon"
__copyright__   = "Copyright 2013, University of Florida"
__license__     = "BSD 3-Clause license"
__version__     = "0.1"

import vivotools as vt
from datetime import datetime



def name_parts(name):
    """
    Given  name string, parse into four elelements -- last, first, middle
    and suffix
    """
    
    def name_inner(name):
        """
        Given a string with first and/or first middle, return first and middle
        """
        first = None
        middle = None
        parts = name.split(' ')
        if len(parts) == 0 or len(parts) == 1:
            first = name
        else:
            first = parts[0]
            middle = ' '.join(parts[1:])
        return [first,middle]

    last = None
    first = None
    middle = None
    suffix = None
    parts = name.split(",")
    if len(parts) == 0:
        last = name
    elif len(parts) == 1:
        last = name
    elif len(parts) == 2:
        last = parts[0]
        [first,middle] = name_inner(parts[1])
    elif len(parts) >= 3:
        last = parts[0]
        [first,middle] = name_inner(parts[1])
        suffix = parts[2]
    return [last,first,middle,suffix]

#
#  Start here
#

print datetime.now(),"Start"
data = vt.read_csv("name-parts.csv")
print datetime.now(),"Source data has",len(data),"elements"
ardf = vt.rdf_header()
srdf = vt.rdf_header()

i = 0

for row in sorted(data.keys()):
    i = i + 1
    [last,first,middle,suffix] = name_parts(data[row]['display_name'])
    print i,data[row]['display_name'],":",last,first,middle,suffix
    uri = data[row]['uri']
    person = vt.get_person(uri)
    if not 'last_name' in person:
        person['last_name'] = None
    if not 'first_name' in person:
        person['first_name'] = None
    if not 'middle_name' in person:
        person['middle_name'] = None
    if not 'name_suffix' in person:
        person['name_suffix'] = None
    [add,sub] = vt.update_data_property(uri,'foaf:lastName',person['last_name'],last)
    ardf = ardf + add
    srdf = srdf + sub
    [add,sub] = vt.update_data_property(uri,'foaf:firstName',person['first_name'],first)
    ardf = ardf + add
    srdf = srdf + sub
    [add,sub] = vt.update_data_property(uri,'vivo:middleName',person['middle_name'],middle)
    ardf = ardf + add
    srdf = srdf + sub
    [add,sub] = vt.update_data_property(uri,'bibo:suffixName',person['name_suffix'],suffix)
    ardf = ardf + add
    srdf = srdf + sub
srdf = srdf + vt.rdf_footer()
ardf = ardf + vt.rdf_footer()
print "<-- Addition RDF -->"
print ardf
print "<-- Subtraction RDF -->"
print srdf
print datetime.now(),"End"


        

                 

                 
