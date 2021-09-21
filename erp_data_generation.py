# Generation of fake customer or supplier data (company name, address, employee data...)
# purpose example: populate ERP database for tests
# helpful literature:
# https://zetcode.com/python/faker/
# https://towardsdatascience.com/how-to-create-fake-data-with-faker-a835e5b7a9d9
# https://medium.com/district-data-labs/a-practical-guide-to-anonymizing-datasets-with-python-faker-ecf15114c9be

import csv
import random
import re
from decode_import_file import read_structure
from erp_basic_tools import CreateFile
from faker import Faker
faker = Faker('de_DE')  # locale for local sounding Names, Companies, Addresses


class GeneratorBase(CreateFile):
    def __init__(self, outputfile, outputfile_structure, count, **kwrest):
        super().__init__(outputfile, outputfile_structure, **kwrest)
        self.count = count

    @staticmethod
    def split_address(address):
        street, postcode_town = address.splitlines()
        postcode, town = postcode_town.split(' ', 1)
        return [street, postcode, town]


class GenerateCompanyData(GeneratorBase):
    def generate(self):
        company_name_and_address = []
        for nn in range(self.count):
            company_name = faker.company()
            company_address = faker.address()
            address_parts = self.split_address(company_address)
            status_customer = random.randint(0, 3)
            status_supplier = random.randint(0, 1)
            company_name_and_address.append([company_name, company_address])
            self.output(company_name, address_parts, status_customer, status_supplier)
        return company_name_and_address

    def output(self, company_name, address_parts, status_customer, status_supplier):
        if not self.testmode:
            company_dict = {'company_name': company_name, 'address_parts\[0\]': address_parts[0],
                            'address_parts\[1\]': address_parts[1], 'address_parts\[2\]': address_parts[2],
                            'status_customer': str(status_customer), 'status_supplier': str(status_supplier)}
            self.output_csv(company_dict)
        else:
            self.output_test(company_name, address_parts, status_customer, status_supplier)

    @staticmethod
    def output_test(company_name, address_parts, status_customer, status_supplier):
        print(f'Firma: {company_name}')
        print(f'Straße, Hausnummer: {address_parts[0]}')
        print(f'PLZ: {address_parts[1]}')
        print(f'Ort: {address_parts[2]}')
        print('+++++++++++++++')


class GeneratePersonData(GeneratorBase):
    def __init__(self, outputfile, outputfile_structure, count, **kwrest):
        super().__init__(outputfile, outputfile_structure, count, **kwrest)
        company = kwrest.get('company', '') #to enable person contacts belonging to a company
        company_address = kwrest.get('company_address', '') #to enable person address equal to company address
        self.company = company
        self.company_address = company_address

    def generate(self):

        nampart = []  # contains patterns to remove prename like elments like Prof.Dr., Frau, Herr, ...
        nampart.append(r"(.*\w+\.)+\s")  # search for title at beginning, indentifier: "." (detects Prof.Dr. ...)
        #nampart.append(r"(^[Prof|Dr]+\.)+\s")  # search for title at beginning, indentifier: "." (detects Prof.Dr. ...)
        nampart.append(r"Frau |Herr ")  # search for "Frau" or "Herr" at beginning

        for nn in range(self.count):

            if self.company == '':  # if company name is empty, a name is being created, but no other company data
                company_name = faker.company()
            else:
                company_name = self.company

            prename = []  # reset prename variable
            person_name = faker.name()
            # print(f'raw Person Name: {person_name}')

            # remove prename elements
            for pattern in nampart:
                mat = re.match(pattern, person_name)
                if mat:
                    prename.append(mat.group())
                    person_name = re.sub(pattern, "", person_name)

            try:  # it occurs that remaining name consists only of one word, so split function will raise ValueError
                first_name, last_name = person_name.split(' ', 1)  # split in first and last name. ToDo: handle double first name
            except(ValueError):
                print(f'Value Error - person name before split: "{person_name}", prename: "{prename}"')
                last_name = person_name
                first_name = ''

            email = faker.ascii_company_email()

            if self.company_address == '':  # if company_address is empty, a company address is being created
                person_address = faker.address()
            else:
                person_address = self.company_address

            address_parts = self.split_address(person_address)
            self.output(company_name, first_name, last_name, address_parts, email)

    def output(self, company_name, first_name, last_name, address_parts, email):
        if not self.testmode:
            person_dict = {'company_name': company_name, 'address_parts\[0\]': address_parts[0],
                           'address_parts\[1\]': address_parts[1], 'address_parts\[2\]': address_parts[2],
                           'first_name': first_name, 'last_name': last_name, 'email': email}
            self.output_csv(person_dict)
        else:
            self.output_test(company_name, first_name, last_name, address_parts, email)

    @staticmethod
    def output_test(company_name, first_name, last_name, address_parts, email):
        # print(f'name: {person_name}')
        # print(f'mat: {mat}')
        # print(f'prename: {prename}')
        print(f'nname: {last_name}')
        print(f'vname: {first_name}')
        print(f'email: {email}')
        # print(f'address: {person_address}')
        print(f'Straße, Hausnummer: {address_parts[0]}')
        # print(f'PLZ Ort: {plz_stadt}')
        print(f'PLZ: {address_parts[1]}')
        print(f'Ort: {address_parts[2]}')
        print(f'Firma: {company_name}')
        print('------------------')


def generate_persondata_and_companydata(count_company, count_person, outputfile_company, outputfile_person,
                                        data_structure, **kwrest):
    test = kwrest.get('test', False)  # in testmode, output is written to display instead of file

    CG = GenerateCompanyData(outputfile_company, data_structure[0], count_company, test=test)
    company_name_and_address = CG.generate()

    for nn in range(count_company):
        for mm in range(random.randint(1, count_person)):
            PG = GeneratePersonData(outputfile_person, data_structure[1], 1, company=company_name_and_address[nn][0],
                                    company_address=company_name_and_address[nn][1], test=test)
            PG.generate()


if __name__ == '__main__':
    GePartnerDatei_Template = '/home/hhhans/Lokal/Labor/Dolibarr/Datenimport/Beispiel_Import_Datei_societe_1.orig.V13.csv'
    GeKontaktDatei_Template = '/home/hhhans/Lokal/Labor/Dolibarr/Datenimport/Beispiel_Import_Datei_societe_2.orig.V13.csv'
    # GePartnerDatei='~/Lokal/Labor/Dolibarr/Datenimport/Beispiel_Import_Datei_societe_1.csv'
    # GeKontaktDatei = '~/Lokal/Labor/Dolibarr/Datenimport/Beispiel_Import_Datei_societe_2.csv'
    GePartnerDatei = 'Beispiel_Import_Datei_societe_1.csv'
    GeKontaktDatei = 'Beispiel_Import_Datei_societe_2.csv'

    mapping1 = {'s.nom': 'company_name', 's.client': 'status_customer', 's.fournisseur': 'status_supplier',
               's.status': '1', 's.code_client': 'auto', 's.code_fournisseur': 'auto', 's.address': 'address_parts[0]',
               's.zip': 'address_parts[1]', 's.town': 'address_parts[2]'}
    mapping2 = {'s.fk_soc': 'company_name', 's.firstname': 'first_name', 's.lastname': 'last_name',
               's.address': 'address_parts[0]', 's.zip': 'address_parts[1]', 's.town': 'address_parts[2]',
               's.email': 'email'}

    data_structure = []
    data_structure.append(read_structure(GePartnerDatei_Template, mapping1))
    # PG = GeneratePersonData(GeKontaktDatei, data_structure, 3)
    # PG.generate()
    data_structure.append(read_structure(GeKontaktDatei_Template, mapping2))
    # CG = GenerateCompanyData(GePartnerDatei, data_structure[0], 3)
    # CG.generate()
    generate_persondata_and_companydata(50, 20, GePartnerDatei, GeKontaktDatei, data_structure, test=False)

