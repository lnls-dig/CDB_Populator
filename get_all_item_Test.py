# -*- coding: utf-8 -*-
"""
Created on Mon May  3 ‎09:30:22 2020

Receptor de dados do ComponentDB

@author: caiom
"""

from cdb.cdb_web_service.api.itemRestApi import ItemRestApi
from cdb.common.exceptions.invalidRequest import InvalidRequest
import pandas as pd
from io import StringIO

#Reads a file with the credentials and save in the "line" variables
data = open('account_cdb.txt', 'r')
line = data.readlines()
user = line[0]
password = line[1]
server = line[2]
port = 10232
protocol = line[4]
data.close

#Log into CDB database and get all catalog items with all properties
login = ItemRestApi(user, password, server, port, protocol)
catalog = login.getCatalogItems()

#'y' will be catalog item property list and 'z' will be 'w' sulfix number.
#Ex: cat0 is equal to a concatenation of y and z (y+z)
w = 'item'
x = 0
y = 'cat'
z = 0

#This loop function maps the catalog dictionaries with the item data and convert into lists which will be saved in the memory
for item in catalog:
    exec(w+str(x)+'=catalog[x]')
    exec('del '+w+str(x)+"[u'domain']")
    exec("if u'item_identifier2' in "+ w+str(x)+ ": del "+ w+str(x) +"[u'item_identifier2']")
    exec(y+str(z)+"="+ w+str(x) +'.values()')
    exec(y+str(z)+".sort(reverse = True)")
    exec("print("+y+str(z)+")")
    x += 1
    z += 1

#Prints a DataFrame of the acquired data in the request
cat_table = pd.DataFrame(cat_list, columns = ['Item Name', 'Item Identifier', 'Item ID', 'Item Domain'])
print(cat_table)
