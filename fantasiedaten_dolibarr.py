# Generation of fake customer or supplier data (company name, address, employee data...)
# purpose example: populate ERP datbase for tests
# helpful literature:
# https://zetcode.com/python/faker/
# https://towardsdatascience.com/how-to-create-fake-data-with-faker-a835e5b7a9d9
# https://medium.com/district-data-labs/a-practical-guide-to-anonymizing-datasets-with-python-faker-ecf15114c9be

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from faker import Faker
faker = Faker('de_DE') #locale for local sounding Names, Companies, Addresses
import csv
import random
import re


class GeneratorBase:
    def __init__(self, outputfile, count, **kwrest):
        testmode = kwrest.get('test', False) #in testmode, output is written to display instead of file
        company = kwrest.get('company', '') #to enable person contacts belonging to a company
        self.testmode = testmode
        self.outputfile = outputfile
        self.count = count
        self.company = company

    def split_address(self, address):
        street, postcode_town = address.splitlines()
        postcode, town = postcode_town.split(' ', 1)
        return [street, postcode, town]


class GenerateCompanyData(GeneratorBase):
    def generate(self):
        aunt = []
        for nn in range(self.count):
            company_name = faker.company()
            company_address = faker.address()
            address_parts = self.split_address(company_address)
            status_customer = random.randint(0, 3)
            status_supplier = random.randint(0, 1)
            aunt.append([company_name, company_address])
            self.output(company_name, address_parts, status_customer, status_supplier)
        return aunt

    def output(self, company_name, address_parts, status_customer, status_supplier):
        if not self.testmode:
            self.output_csv(company_name, address_parts, status_customer, status_supplier)
        else:
            self.output_test(company_name, address_parts, status_customer, status_supplier)

    def output_csv(self, company_name, address_parts, status_customer, status_supplier):
        with open(self.outputfile, 'a+', newline='') as csvfile:
            dbwriter = csv.writer(csvfile, delimiter=',',
                                  quotechar='|', quoting=csv.QUOTE_MINIMAL)
            dbwriter.writerow([company_name] + [''] + [1] + ['"auto"'] * 2 + [''] * 2 + [address_parts[0]] +
                              [address_parts[1]] + [address_parts[2]] +
                              [''] * 21 + [status_customer] + [status_supplier] + [''] * 12)

    @staticmethod
    def output_test(company_name, address_parts, status_customer, status_supplier):
        print(f'Firma: {company_name}')
        print(f'Straße, Hausnummer: {address_parts[0]}')
        print(f'PLZ: {address_parts[1]}')
        print(f'Ort: {address_parts[2]}')
        print('+++++++++++++++')


class GeneratePersonData(GeneratorBase):
    def generate(self):

        nampart = []  # contains patterns to remove prename like elments like Prof.Dr., Frau, Herr, ...
        nampart.append(r"(.*\w+\.)+\s")  # search for title at beginning, indentifier: "." (detects Prof.Dr. ...)
        nampart.append(r"Frau|Herr")  # search for "Frau" or "Herr" at beginning

        for nn in range(self.count):
            if self.company == '':  # if company name is empty, a company name is being created, but no other company data
                company_name = faker.company()
            else:
                company_name = self.company

            prename = []  # reset prename variable
            person_name = faker.name()

            # remove prename elements
            for pattern in nampart:
                mat = re.match(pattern, person_name)
                if mat:
                    prename.append(mat.group())
                    person_name = re.sub(pattern, "", person_name)

            first_name, last_name = person_name.split(' ', 1)  # split in first and last name. ToDo: handle double first name
            email = faker.ascii_company_email()
            person_address = faker.address()
            address_parts = self.split_address(person_address)
            self.output(company_name, first_name, last_name, address_parts, email)

    def output(self, company_name, first_name, last_name, address_parts, email):
        if not self.testmode:
            self.output_csv(company_name, first_name, last_name, address_parts, email)
        else:
            self.output_test(company_name, first_name, last_name, address_parts, email)

    def output_csv(self, company_name, first_name, last_name, address_parts, email):
        with open(self.outputfile, 'a+', newline='') as csvfile:
            dbwriter = csv.writer(csvfile, delimiter=',',
                                  quotechar='|', quoting=csv.QUOTE_MINIMAL)
            dbwriter.writerow(
                [''] + [''] + [company_name] + [''] + [last_name] + [first_name] + [address_parts[0]] +
                      [address_parts[1]] + [address_parts[2]] + [''] * 8 + [email] + [''] * 3)

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


def kontakte(anz, kontaktdatei, **kwrest):
    # firmendatei = rest[1]
    if 'test' not in kwrest:
        test = False
    else:
        test = kwrest.get('test')

    nampart = [] # contains patterns to remove prename like elments like Prof.Dr., Frau, Herr, ...
    nampart.append(r"(.*\w+\.)+\s") # search for title at beginning, indentifier: "."
    nampart.append(r"Frau|Herr")  # search for "Frau" or "Herr" at beginning

    for nn in range(anz):
        if 'unt' not in kwrest:
            unt = faker.company()
        else:
            unt = kwrest.get('unt')

        prename = [] # reset prename variable
        nam = faker.name()
        #namt = nam.split(' ', 1)

        # remove prename elements
        for pattern in nampart:
            mat = re.match(pattern, nam)
            if mat:
                prename.append(mat.group())
                nam = re.sub(pattern, "", nam)

        vnam, nnam = nam.split(' ', 1) #split in first and last name. ToDo: handle double first name
        email = faker.ascii_company_email()
        add = faker.address()
        stra, plz_stadt = add.splitlines()
        plz, stadt = plz_stadt.split(' ', 1)

        if not test:
            with open(kontaktdatei, 'a+', newline='') as csvfile:
                dbwriter = csv.writer(csvfile, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                # dbwriter.writerow([nam] + [''] * 30 + ['2'] + ['0'])
                dbwriter.writerow([''] + [''] + [unt] + [''] + [nnam] + [vnam] + [stra] + [plz] + [stadt] + [''] * 8 + [email] + [''] * 3)
        else:
            print(f'name: {nam}')
            print(f'mat: {mat}')
            print(f'prename: {prename}')
            print(f'nname: {nnam}')
            print(f'vname: {vnam}')
            print(f'email: {email}')
            print(f'address: {add}')
            print(f'Straße, Hausnummer: {stra}')
            print(f'PLZ Ort: {plz_stadt}')
            print(f'PLZ: {plz}')
            print(f'Ort: {stadt}')
            print(f'Firma: {unt}')
            print('------------------')

def firmen_kontakte(anzf, anzk, firmendatei, kontaktdatei, **kwrest):
    if 'ftest' not in kwrest:
        ftest = False
    else:
        ftest = kwrest.get('ftest')

    CG = GenerateCompanyData(firmendatei, anzf, test=ftest)
    aunt = CG.generate()
    #aunt = firmen(anzf, firmendatei, ftest=test)
    for nn in range(anzf):
        for mm in range(random.randint(1, anzk)):
            nam = faker.name()
            vnam, nnam = nam.split(' ', 1)
            email = faker.ascii_company_email()
            unt = aunt[nn][0]
            add = aunt[nn][1]
            stra, plz_stadt = add.splitlines()
            plz, stadt = plz_stadt.split(' ', 1)

            if not ftest:
                with open(kontaktdatei, 'a+', newline='') as csvfile:
                    dbwriter = csv.writer(csvfile, delimiter=',',
                                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    # dbwriter.writerow([nam] + [''] * 30 + ['2'] + ['0'])
                    dbwriter.writerow([''] + [''] + [unt] + [''] + [nnam] + [vnam] + [stra] + [plz] + [stadt] + [''] * 8 + [email] + [''] * 3)
            else:
                print(f'nname: {nnam}')
                print(f'vname: {vnam}')
                print(f'email: {email}')
                # print(f'address: {add}')
                print(f'Straße, Hausnummer: {stra}')
                # print(f'PLZ Ort: {plz_stadt}')
                print(f'PLZ: {plz}')
                print(f'Ort: {stadt}')
                print(f'Firma: {unt}')
                print('------------------')

if __name__ == '__main__':
    schreib = False;
    # GePartnerDatei='/home/hhhans/Lokal/Labor/Dolibarr/Datenimport/Beispiel_Import_Datei_societe_1.csv'
    # GeKontaktDatei = '/home/hhhans/Lokal/Labor/Dolibarr/Datenimport/Beispiel_Import_Datei_societe_2.csv'
    GePartnerDatei='Beispiel_Import_Datei_societe_1.csv'
    GeKontaktDatei = 'Beispiel_Import_Datei_societe_2.csv'
    # au = firmen(5, GePartnerDatei, test=True)
    # print(au)
    #kontakte(5, GeKontaktDatei, test=True)
    # firmen_kontakte(2, 3, GePartnerDatei, GeKontaktDatei, ftest=False)
    PG = GeneratePersonData(GeKontaktDatei, 3, test=False)
    PG.generate()

