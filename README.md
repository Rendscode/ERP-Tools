# FakeDataCreation

## Keywords: Dolibarr, ERP, company data, test

This set of functions creates fake data for the open source ERP System dolibarr. Currently data can be created for instances of companies and (person) contacts within these companies.

## Motivation
In order to demonstrate the capabilities of Dolibarr to prospects it's helpful to have a significant number of (dummy) contacts with different categories
(customer, prospect, supplier; active / inactive...). This helps showing also the performance of a web hosted database with a large number of contacts.

## Usage

### Localisation
To have realistic looking data, the faker module is used. Faker can be customized to output data in country specific format and content: company and person names, civility of persons, address format, regional city names. To localize to your needs change the faker locale.

### Output to file - import file format of Dolibarr
Dolibarr can input data via .csv files. In Dolibarr it's possible to trigger the output of a template file. The structure of the file (entries and order of the entries in columns) can change from version to version. To easily obtain the structure use the **read_structure** function

### Generate company data



## ToDos:

