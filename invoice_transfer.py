# This file helps transfer supplier invoice data from a Libre Office ODB Database to the ERP System Dolibarr
# via Dolibarr's spreadsheet import functionality

from decode_import_file import read_structure  # function to determine data order in spreadsheet
# import csv
import re
import pandas as pd
from erp_basic_tools import CreateFile

class TransferSupplierInvoices(CreateFile):
    def __init__(self, input_data, outputfile_invoice, outputfile_structure_invoice, outputfile_invoice_items, outputfile_structure_invoice_items, **kwrest):
        testmode = kwrest.get('test', False)  # in testmode, output is written to display instead of file
        self.testmode = testmode
        self.input_data = input_data
        self.outputfile_invoice = outputfile_invoice
        self.outputfile_structure_invoice = outputfile_structure_invoice
        self.outputfile_invoice_items = outputfile_invoice_items
        self.outputfile_structure_invoice_items = outputfile_structure_invoice_items


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    data_from_libreoffice = '/home/hhhans/Lokal/Dolibarr/Datenmigration KalkulationWattwurm/Export aus KalkulationWattwurmDB.csv'
    supplier_invoice_template = '/home/hhhans/Lokal/Dolibarr/Datenmigration KalkulationWattwurm/Beispiel_Import_Datei_fournisseur_1.V14.csv'
    supplier_invoice_items_template = '/home/hhhans/Lokal/Dolibarr/Datenmigration KalkulationWattwurm/Beispiel_Import_Datei_fournisseur_2.V14.csv'

    output_file_supplier_invoice = 'Import_Datei_fournisseur_1.V14.csv'
    output_file_supplier_invoice_items = 'Import_Datei_fournisseur_2.V14.csv'

    mapping_supplier_invoice_template = {
        'f.ref': 'invoice_number_gen',
        'f.ref_supplier': 'invoice_number_db',
        'f.type': '0',
        'f.fk_soc': 'supplier_name_db',
        'f.datec': '',
        'f.datef': 'invoice_date_db',
        'f.date_lim_reglement': '',
        'f.total_ht': 'price_excl_vat',
        'f.total_ttc': 'price_incl_vat',
        'f.total_tva': 'amount_vat',
        'f.paye': '1',
        'f.fk_statut': '2',
        'f.fk_user_modif': '',
        'f.fk_user_valid': '',
        'f.fk_facture_source': '',
        'f.fk_projet': '',
        'f.fk_account': '2',
        'f.note_public': '',
        'f.note_private': '',
        'f.fk_cond_reglement': '',
        'f.fk_mode_reglement': '',
        'f.model_pdf': '',
        'f.date_valid': ''
        }

    mapping_supplier_invoice_items_template = {
        'fd.fk_facture_fourn': 'invoice_number_gen',
        'fd.fk_parent_line': '',
        'fd.fk_product': '',
        'fd.label': '',
        'fd.description': 'item',
        'fd.pu_ht': 'item_price_excl_vat',
        'fd.pu_ttc': 'item_price_incl_vat',
        'fd.qty': 'item_count',
        'fd.remise_percent': '',
        'fd.vat_src_code': '',
        'fd.product_type': '',
        'fd.tva_tx': '',
        'fd.total_ht': '',
        'fd.tva': '',
        'fd.total_ttc': '',
        'fd.date_start': '',
        'fd.date_end': '',
        'fd.fk_unit': '',
        'extra.kostenart': 'cost_class',
        'extra.zusatzschluessel': 'supplementary_key',
        'extra.steuerkategorie': 'tax_class',
        'extra.privatanteil': 'tax_private_ratio',
        'extra.anmerkung': 'annotation',
        'extra.steuerjahr': 'taxation_year'
        }


    data_structure = []
    data_structure.append(read_structure(supplier_invoice_template, mapping_supplier_invoice_template))

    data_structure.append(read_structure(supplier_invoice_items_template, mapping_supplier_invoice_items_template))

    input_data_df = pd.read_csv(data_from_libreoffice, sep=';')
    # print(input_data_df.tail(30))
    print(input_data_df.info())
    #print(input_data_df.groupby(['Datum', 'Rechnungssteller']).median()
    #print(input_data_df.pivot(index='Datum', columns='Rechnungssteller', values=['Posten']))
    tbl = pd.pivot_table(input_data_df, index=['Datum','Rechnungssteller'], columns=['Posten', 'Anzahl'])
    print(tbl.info())


    InvoiceTransfer = TransferSupplierInvoices(input_data_df, output_file_supplier_invoice, data_structure[0], output_file_supplier_invoice_items, data_structure[1])
    # IT = InvoiceTransfer.input_db()

    print("Ende!")

