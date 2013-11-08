vivo-name-parts
===============

Add name parts to VIVO for people with a display name, but no name parts

People in VIVO are expected to have name parts -- first name, last name, middle name or initial and name prefix and/or name suffix.

name-parts.py reads a CSV file name-parts.csv, that has two columns
- uri.  The uri of the person whose name parts will be updated
- display-name.  A name for the person of the form last, first middle, suffix.  UF does not have prefixes in display names

name-parts.py reads the CSV, and parses each display name into name parts.  It uses get_person from vivotools to retrive the 
person's existing name parts, if any.  It uses update_data_proptery from vivotools to generate addition and subtraction RDF as necessary to update the last, first, middle and suffix names of the people in the CSV file.

Because get_person and update_data_property are used, name-parts will update values it finds in VIVO, considering the CSV file as the authoritative source.  If VIVO does not have a value for a property, the value from the CSV will be *added*.  If VIVO has a value, it will be *subtracted* and the value from the CSV will be *added*.  If VIVO has a value and the CSV does not, the value in VIVO will be *subtracted*.  In all cases, the CSV is authoritative.

name-parts.rq is a SPARQL query that can be used to find all the UF people in VIVO that do not have name parts.  The uri of the person and their display name (stored in rdfs:label) are retrieved.  The output of the query should be saved as name-parts.csv and used as input to name-parts.py

# Steps for running name-parts.py

1. Run name-parts.rq and store the resulting CSV as name-parts.csv
2. Edit name-parts.csv to add a header withthe columns names uri,display_name
3. Run name-parts.py to produce a python log file
4. Save the first part of the log as name-parts.log
5. Save the second part as name-parts-add.rdf
6. Save the third part as name-parts-sub.rdf
7. Add the addition RDF (name-parts-add.rdf) to VIVO through the admin interface
8. Add the subtraction RDF (name-parts-sub.rdf) to VIVO throgh the admin interface

Voila!  Name parts have been added to VIVO for anyone who was missing name parts.

M. Conlon November 8, 2013
