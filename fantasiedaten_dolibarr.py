# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from faker import Faker
faker = Faker('de_DE')
import csv
import random
# import re

def firmen(anz, firmendatei, **kwrest):
    aunt = []
    if 'ftest' not in kwrest:
        ftest = False
    else:
        ftest = kwrest.get('ftest')

    for nn in range(anz):
        unt = faker.company()
        add = faker.address()
        stra, plz_stadt = add.splitlines()
        plz, stadt = plz_stadt.split(' ', 1)
        stkd = random.randint(0, 3)
        stlf = random.randint(0, 1)
        aunt.append([unt, add])

        if not ftest:
            with open(firmendatei, 'a+', newline='') as csvfile:
                dbwriter = csv.writer(csvfile, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                # dbwriter.writerow([nam] + [''] * 30 + ['2'] + ['0'])
                dbwriter.writerow([unt] + [''] + [1] + ['"auto"'] * 2 + [''] * 2 + [stra] + [plz] + [stadt] + [''] * 21
                                  + [stkd] + [stlf] + [''] * 12)
        else:
            print(f'Firma: {unt}')
            # print(f'address: {add}')
            print(f'Straße, Hausnummer: {stra}')
            # print(f'PLZ Ort: {plz_stadt}')
            print(f'PLZ: {plz}')
            print(f'Ort: {stadt}')
            print('+++++++++++++++')
    return aunt


def kontakte(anz, kontaktdatei, **kwrest):
    # firmendatei = rest[1]
    if 'test' not in kwrest:
        test = False
    else:
        test = kwrest.get('test')

    for nn in range(anz):
        if 'unt' not in kwrest:
            unt = faker.company()
        else:
            unt = kwrest.get('unt')

        nam = faker.name()
        namt = nam.split(' ', 1)
        vnam, nnam = nam.split(' ', 1)
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
    if 'test' not in kwrest:
        test = False
    else:
        test = kwrest.get('test')

    aunt = firmen(anzf, firmendatei, ftest=test)
    for nn in range(anzf):
        for mm in range(random.randint(1, anzk)):
            nam = faker.name()
            vnam, nnam = nam.split(' ', 1)
            email = faker.ascii_company_email()
            unt = aunt[nn][0]
            add = aunt[nn][1]
            stra, plz_stadt = add.splitlines()
            plz, stadt = plz_stadt.split(' ', 1)

            if not test:
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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    schreib = False;
    GePartnerDatei='/home/hhhans/Lokal/Labor/Dolibarr/Datenimport/Beispiel_Import_Datei_societe_1.csv'
    GeKontaktDatei = '/home/hhhans/Lokal/Labor/Dolibarr/Datenimport/Beispiel_Import_Datei_societe_2.csv'
    # au = firmen(5, GePartnerDatei, test=True)
    # print(au)
    kontakte(5, GeKontaktDatei, test=True)
    # firmen_kontakte(40, 30, GePartnerDatei, GeKontaktDatei, test=False)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
