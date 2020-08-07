# -*- coding: utf-8 -*-
"""
Created on Mon, May 18 ‎09:30:22 2020

ComponentDB Catalog Items Receiver

@author: Caio Santos - DIG
"""

from cdb.cdb_web_service.api.itemRestApi import ItemRestApi
from cdb.common.exceptions.invalidRequest import InvalidRequest
import pandas as pd
import getpass

print("INSERT CDB CREDENTIALS\n")

#Reads the credentials and save in the variables to connect to the server
protocol = raw_input("\nNetwork protocol: ")
server = raw_input("CDB server: ")
port = int(input("Server port: "))
user = raw_input("CDB user name: ")
password = getpass.getpass(prompt = "Password: ")
print("\nLoading data...\n")

#Log into CDB database
login = ItemRestApi(user, password, server, port, protocol)

#Defines a function to get catalog from the server
def get_catalog():

#Calls the function from CDB API
    print('Loading catalog items...\n')
    catalog = login.getCatalogItems()
    cat_list = []

#loop to map the catalog item data dictionaries and convert into lists
    for i in range(0, len(catalog)):
        if u'domain' in catalog[i]:
            del catalog[i][u'domain']
        if u'item_identifier2' in catalog[i]:
            del catalog[i][u'item_identifier2']

        item = [catalog[i][u'name'], catalog[i][u'item_identifier1'], catalog[i][u'id'], catalog[i][u'domain_id']]
        cat_list.append(item)

    table = pd.DataFrame(cat_list, columns = ['Item Name', 'Item Identifier', 'Item ID', 'Item Domain'])
    pd.set_option('max_columns', 5)
    pd.set_option('max_colwidth', 200)

    print(table)

get_catalog()
