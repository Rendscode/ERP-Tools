# Generation of fake customer or supplier data (company name, address, employee data...)
# purpose example: populate ERP database for tests
# helpful literature:
# https://zetcode.com/python/faker/
# https://towardsdatascience.com/how-to-create-fake-data-with-faker-a835e5b7a9d9
# https://medium.com/district-data-labs/a-practical-guide-to-anonymizing-datasets-with-python-faker-ecf15114c9be

import csv
import random
import re
from faker import Faker
faker = Faker('de_DE') #locale for local sounding Names, Companies, Addresses


class GeneratorBase:
    def __init__(self, outputfile, count, **kwrest):
        testmode = kwrest.get('test', False) #in testmode, output is written to display instead of file
        self.testmode = testmode
        self.outputfile = outputfile
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
    def __init__(self, outputfile, count, **kwrest):
        super().__init__(outputfile, count, **kwrest)
        company = kwrest.get('company', '') #to enable person contacts belonging to a company
        company_address = kwrest.get('company_address', '') #to enable person address equal to company address
        self.company = company
        self.company_address = company_address

    def generate(self):

        nampart = []  # contains patterns to remove prename like elments like Prof.Dr., Frau, Herr, ...
        nampart.append(r"(.*\w+\.)+\s")  # search for title at beginning, indentifier: "." (detects Prof.Dr. ...)
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

            first_name, last_name = person_name.split(' ', 1)  # split in first and last name. ToDo: handle double first name
            email = faker.ascii_company_email()

            if self.company_address == '':  # if company_address is empty, a company address is being created
                person_address = faker.address()
            else:
                person_address = self.company_address

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


def generate_persondata_and_companydata(count_company, count_person, outputfile_company, outputfile_person, **kwrest):
    test = kwrest.get('test', False)  # in testmode, output is written to display instead of file

    CG = GenerateCompanyData(outputfile_company, count_company, test=test)
    company_name_and_address = CG.generate()

    for nn in range(count_company):
        for mm in range(random.randint(1, count_person)):
            PG = GeneratePersonData(outputfile_person, 1, company=company_name_and_address[nn][0],
                                    company_address=company_name_and_address[nn][1], test=test)
            PG.generate()


if __name__ == '__main__':
    # GePartnerDatei='~/Lokal/Labor/Dolibarr/Datenimport/Beispiel_Import_Datei_societe_1.csv'
    # GeKontaktDatei = '~/Lokal/Labor/Dolibarr/Datenimport/Beispiel_Import_Datei_societe_2.csv'
    GePartnerDatei='Beispiel_Import_Datei_societe_1.csv'
    GeKontaktDatei = 'Beispiel_Import_Datei_societe_2.csv'
    # au = firmen(5, GePartnerDatei, test=True)
    # print(au)
    #kontakte(5, GeKontaktDatei, test=True)
    #generate_persondata_and_companydata(2, 3, GePartnerDatei, GeKontaktDatei, test=False)
    PG = GeneratePersonData(GeKontaktDatei, 3, test=True)
    PG.generate()

