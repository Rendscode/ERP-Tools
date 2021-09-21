# This file helps transfer supplier invoice data from a Libre Office ODB Database to the ERP System Dolibarr
# via Dolibarr's spreadsheet import functionality

from decode_import_file import read_structure  # function to determine data order in spreadsheet
import csv
import re
from erp_basic_tools import CreateFile

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    supplier_invoice_template = '/home/hhhans/Lokal/Dolibarr/Datenmigration KalkulationWattwurm/Beispiel_Import_Datei_fournisseur_1.V14.csv'
    supplier_invoice_items_template = '/home/hhhans/Lokal/Dolibarr/Datenmigration KalkulationWattwurm/Beispiel_Import_Datei_fournisseur_2.V14.csv'
    # GePartnerDatei='~/Lokal/Labor/Dolibarr/Datenimport/Beispiel_Import_Datei_societe_1.csv'
    # GeKontaktDatei = '~/Lokal/Labor/Dolibarr/Datenimport/Beispiel_Import_Datei_societe_2.csv'
    GePartnerDatei = 'Beispiel_Import_Datei_societe_1.csv'
    GeKontaktDatei = 'Beispiel_Import_Datei_societe_2.csv'

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

    # mapping1 = {'s.nom': 'company_name', 's.client': 'status_customer', 's.fournisseur': 'status_supplier',
    #            's.status': '1', 's.code_client': 'auto', 's.code_fournisseur': 'auto', 's.address': 'address_parts[0]',
    #            's.zip': 'address_parts[1]', 's.town': 'address_parts[2]'}
    # mapping2 = {'s.fk_soc': 'company_name', 's.firstname': 'first_name', 's.lastname': 'last_name',
    #            's.address': 'address_parts[0]', 's.zip': 'address_parts[1]', 's.town': 'address_parts[2]',
    #            's.email': 'email'}

    data_structure = []
    data_structure.append(read_structure(supplier_invoice_template, mapping_supplier_invoice_template))

    data_structure.append(read_structure(supplier_invoice_items_template, mapping_supplier_invoice_items_template))

    print("Ende!")

