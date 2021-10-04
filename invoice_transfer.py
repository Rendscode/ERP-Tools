# This file helps transfer supplier invoice data from a Libre Office ODB Database to the ERP System Dolibarr
# via Dolibarr's spreadsheet import functionality

from decode_import_file import read_structure  # function to determine data order in spreadsheet
# import csv
import re
import pandas as pd
from erp_basic_tools import CreateFile, generate_transaction_number

class TransferSupplierInvoices(CreateFile):
    def __init__(self, input_data, outputfile_invoice, outputfile_structure_invoice, outputfile_invoice_items, outputfile_structure_invoice_items, **kwrest):
        super().__init__(outputfile_invoice, outputfile_structure_invoice, **kwrest)
        testmode = kwrest.get('test', False)  # in testmode, output is written to display instead of file
        self.testmode = testmode
        self.input_data = input_data
        self.outputfile_invoice = outputfile_invoice
        self.outputfile_structure_invoice = outputfile_structure_invoice
        self.outputfile_invoice_items = outputfile_invoice_items
        self.outputfile_structure_invoice_items = outputfile_structure_invoice_items


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
        'extra.zusatzschluessel': 'auxiliary_key',
        'extra.steuerkategorie': 'tax_class',
        'extra.privatanteil': 'tax_private_ratio',
        'extra.anmerkung': 'annotation',
        'extra.steuerjahr': 'taxation_year'
        }


    data_structure = []
    data_structure.append(read_structure(supplier_invoice_template, mapping_supplier_invoice_template))

    data_structure.append(read_structure(supplier_invoice_items_template, mapping_supplier_invoice_items_template))

    input_data_df = pd.read_csv(data_from_libreoffice, sep=';', decimal=',', dayfirst=True, parse_dates=["Datum"])

    input_data_grp = input_data_df.groupby(['Datum', 'Rechnungssteller'])

    transaction_number = 1
    InvoiceTransfer = TransferSupplierInvoices(input_data_df, output_file_supplier_invoice, data_structure[0], output_file_supplier_invoice_items, data_structure[1])


    for (Datum, Rechnungssteller), frame in input_data_grp:
    #     print(Rechnungssteller, frame.Einzelpreis, frame.Anzahl, frame.Einzelpreis * frame.Anzahl, end="\n\n")
        invoice_number_gen = generate_transaction_number('LR-{0000}', transaction_number)
        transaction_number += 1

        # data for supplier_invoice
        invoice_number_db = str(pd.unique(frame.Rechnungsnummer.values)[0])
        supplier_name_db = str(pd.unique(frame.Rechnungssteller.values)[0])
        invoice_date_db = frame.Datum.values
        amount_price = frame.Einzelpreis.values * frame.Anzahl.values
        price_excl_vat_array = amount_price if (bool(frame.Mehrwertsteuer.values is True)) else amount_price / 1.19
        price_excl_vat = price_excl_vat_array.sum().round(2)
        price_incl_vat_array = price_excl_vat_array * 1.19  # it would have been less code to just mutliply price_excl_vat by vat_rate, but the chosen solution should be nmore precise in terms of results
        price_incl_vat = price_incl_vat_array.sum().round(2)
        amount_vat = round(price_incl_vat - price_excl_vat, 2)

        print(invoice_number_gen, invoice_number_db, pd.unique(supplier_name_db), pd.unique(invoice_date_db),
          price_excl_vat_array, price_excl_vat, end='\n')

        supplier_invoice_dict = {'invoice_number_gen': invoice_number_gen, 'invoice_number_db': invoice_number_db,
                        'supplier_name_db': supplier_name_db, 'invoice_date_db': str(pd.to_datetime(invoice_date_db).date[0]),
                        'price_excl_vat': str(price_excl_vat), 'price_incl_vat': str(price_incl_vat), 'amount_vat': str(amount_vat)}
        #InvoiceTransfer.output_csv(supplier_invoice_dict)

        # data for supplier_invoice_items
        item = frame.Posten.values
        item_price_excl_vat = price_excl_vat_array.round(2)
        item_price_incl_vat = price_incl_vat_array.round(2)
        item_count = frame.Anzahl.values
        cost_class = frame.Kostenart.values
        auxiliary_key = frame.Zusatzschlüssel.values
        tax_class = frame.Steuerkategorie.values
        tax_private_ratio = frame.Privatanteil.values
        annotation = frame.Anmerkung.values
        taxation_year = frame.Steuerjahr.values

        supplier_invoice_item_dict = {'invoice_number_gen': invoice_number_gen, 'item': item,
                                 'item_price_excl_vat': str(item_price_excl_vat),
                                 'item_price_incl_vat': str(item_price_incl_vat),
                                 'cost_class': cost_class, 'auxiliary_key': auxiliary_key,
                                 'tax_class': tax_class, 'tax_private_ratio': tax_private_ratio,
                                 'annotation': annotation, 'taxation_year': taxation_year
                                 }
        pass

    print("Ende!")

