# contains basic functionality for erp data generation and transfer

import re
import csv

class CreateFile:
    def __init__(self, outputfile, outputfile_structure, **kwrest):
        testmode = kwrest.get('test', False)  # in testmode, output is written to display instead of file
        self.testmode = testmode
        self.outputfile = outputfile
        self.outputfile_structure = outputfile_structure

    # replace dummy entries in output file (like 'company_name') with actual data
    def replace_strings_variables(self, variable_dict):
        outputfile_structure = self.outputfile_structure
        for key, value in variable_dict.items():
            outputfile_structure = re.sub(key, value, str(outputfile_structure))
        return outputfile_structure

    def output_csv(self, output_dict):
        row_output = self.replace_strings_variables(output_dict)  # replace strings in document raw structure with created oontent
        with open(self.outputfile, 'a+', newline='') as csvfile:
            dbwriter = csv.writer(csvfile, delimiter=',',
                                  quotechar='|', quoting=csv.QUOTE_MINIMAL)
            dbwriter.writerow(eval(row_output))
