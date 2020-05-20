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
import numpy as np

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


x = 0
for item in catalog:
    y = 'item'
    exec(y+str(x)+'=catalog[x]')
    exec('del '+ y+str(x) +'[' + 'u' + "'domain'" +']')
    exec('print('+ y+str(x) +'.values())')
    x += 1
