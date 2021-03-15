# since the import file structure is changing over different versions of Dolibarr, these functions help extract
# the respective order
# the data_of_interest dictionary contains the relation between unique identifiers in Dolibarr and the name convention
# of this module

import csv
import re

def read_structure(template_file, data_of_interest):
    with open(template_file, newline='') as csvfile:
        content = csv.reader(csvfile, delimiter=',', quotechar='|')
        headline = content.__next__()
        position = ['' for nn in range(len(headline))]  # list initialization with empty strings

        for data_of_interest_key, data_of_interest_value in data_of_interest.items():
            index = 0
            for field in headline:
                mat = re.search(data_of_interest_key, field)
                if mat:
                    position[index] = (data_of_interest_value)
                index += 1

        print(position)

if __name__ == '__main__':
    GePartnerDatei = '/home/hhhans/Lokal/Labor/Dolibarr/Datenimport/Beispiel_Import_Datei_societe_1.orig.V12.csv'

    mapping = {'s.nom': 'company_name', 's.client': 'status_customer', 's.fournisseur': 'status_supplier',
               's.status': '1', 's.code_client': 'auto', 's.code_fournisseur': 'auto', 's.address': 'address_parts[0]',
               's.zip': 'address_parts[1]', 's.town': 'address_parts[2]'}

    read_structure(GePartnerDatei, mapping)
