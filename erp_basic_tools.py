# contains basic functionality for erp data generation and transfer

import re
import csv

class CreateFile:
    def __init__(self, outputfile, outputfile_structure, **kwrest):
        testmode = kwrest.get('test', False)  # in testmode, output is written to display instead of file
        self.testmode = testmode
        self.outputfile = outputfile
        #        outputfile_structure = kwrest.get('outputfile_structure', '')
        self.outputfile_structure = outputfile_structure

    # replace dummy entries in output file (like 'company_name') with actual data
    def replace_strings_variables(self, variable_dict):
        outputfile_structure = self.outputfile_structure
        for key, value in variable_dict.items():
            outputfile_structure = re.sub(key, value, str(outputfile_structure))
        return outputfile_structure

    def output_csv(self, output_dict):
        # company_dict = {'company_name': company_name, 'address_parts\[0\]': address_parts[0],
        #                 'address_parts\[1\]': address_parts[1], 'address_parts\[2\]': address_parts[2],
        #                 'status_customer': str(status_customer), 'status_supplier': str(status_supplier)}
        row_output = self.replace_strings_variables(output_dict)  # replace strings in document raw structure with created oontent
        with open(self.outputfile, 'a+', newline='') as csvfile:
            dbwriter = csv.writer(csvfile, delimiter=',',
                                  quotechar='|', quoting=csv.QUOTE_MINIMAL)
            dbwriter.writerow(eval(row_output))

    # def output_csv(self, company_name, address_parts, status_customer, status_supplier):
    #     company_dict = {'company_name': company_name, 'address_parts\[0\]': address_parts[0],
    #                     'address_parts\[1\]': address_parts[1], 'address_parts\[2\]': address_parts[2],
    #                     'status_customer': str(status_customer), 'status_supplier': str(status_supplier)}
    #     row_output = self.replace_strings_variables(
    #         company_dict)  # replace strings in document raw structure with created oontent
    #     with open(self.outputfile, 'a+', newline='') as csvfile:
    #         dbwriter = csv.writer(csvfile, delimiter=',',
    #                               quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #         dbwriter.writerow(eval(row_output))