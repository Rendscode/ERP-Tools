# contains basic functionality for erp data generation and transfer

import re

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