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
from collections import OrderedDict

print("\n"+"**"*20+" CDB CATALOG ITEMS "+"**"*20+"\n\nINSERT CDB CREDENTIALS")

#Reads the credentials and save in the variables to connect to the server
protocol = raw_input("\nNetwork protocol: ")
server = raw_input("CDB server: ")
port = int(input("Server port: "))
user = raw_input("CDB user name: ")
password = getpass.getpass(prompt = "Password: ")
print("\nLoading data...\n")

#Log into CDB database and get all catalog items with all properties
login = ItemRestApi(user, password, server, port, protocol)

#Defines a function to get catalog from the server and store in a list of lists
def get_catalog():
    global catalog
    global cat_list
    global cat_table
    global cat_id

#Calls the function from CDB API
    catalog = login.getCatalogItems()
    w = 'item'
    x = 0
    y = 'cat'
    z = 0
    cat_list = []

#loop to map the catalog item data dictionaries and convert into lists which will be saved in the memory
    for item in catalog:
        exec(w+str(x)+'=catalog[x]')
        exec("if u'domain' in "+w+str(x)+": del "+w+str(x)+"[u'domain']")
        exec("if u'item_identifier2' in "+ w+str(x)+ ": del "+ w+str(x) +"[u'item_identifier2']")
        exec(y+str(z)+'=OrderedDict(sorted('+w+str(x)+'.items(), reverse=True))')
        exec("cat_list.append("+y+str(z)+".values())")
        x += 1
        z += 1

#Defines a function to receive the catalog and print it
def print_catalog():
    get_catalog()
    cat_table = pd.DataFrame(cat_list, columns = ['Item Name', 'Item Identifier', 'Item ID', 'Item Domain'])
    print("**"*20+" CATALOG ITEMS LIST "+"**"*20+"\n")
    print(cat_table)

print_catalog()
