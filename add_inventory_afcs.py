# -*- coding: utf-8 -*-
"""
Created on Tue, May 19 ‎12:14:25 2020

CDB Add Item

@author: Caio Santos - DIG
"""

import cdb
from cdb.cdb_web_service.api.itemRestApi import ItemRestApi
from cdb.common.exceptions.invalidRequest import InvalidRequest
from cdb.common.exceptions.objectNotFound import ObjectNotFound
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import load_workbook
import pandas as pd
import unidecode
import getpass

print("\n"+"**"*20+" CDB ADD ITEMS "+"**"*20+"\n\nINSERT CDB CREDENTIALS")
#Reads the credentials and save in the variables to connect to the server
protocol = raw_input("\nNetwork protocol: ")
server = raw_input("CDB server: ")
port = int(input("Server port: "))
user = raw_input("CDB user name: ")
password = getpass.getpass(prompt = "Password: ")

#Log into CDB database
login = ItemRestApi(user, password, server, port, protocol)

#Opens a Excel sheet to receive the inventory items data and save as a workbook
pd.set_option('max_colwidth', 80)
plan = pd.ExcelFile(r'/mnt/c/Users/caiom/Documents/CDB Document Files/Codes/controle_config_sirius_ebpm_total.xlsx')
ex = pd.read_excel(plan, dtype = { 'SN' : str })

wb = Workbook()
ws = wb.active

for r in dataframe_to_rows(ex, index=True, header=True):
    ws.append(r)

wb.save('afc_plan.xlsx')

exemplo1 = load_workbook('afc_plan.xlsx', read_only=True)
sheet = exemplo1['Sheet']

afc = []

#Reads the Excel and get the useful data
for data in ws.iter_rows(values_only=True):
    if 'AFC' not in data:
        continue
    ipn = data[1]+':'+data[3]+':'+data[2]
    sn = data[5]
    obs = data[28]
    afc.append((ipn, sn, obs))

#Validate inventory item existance

#For AFCs
    if ":3.1:" in ipn:
        try:
            login.getItemByUniqueAttributes('Inventory', ipn, itemIdentifier1 = sn, derivedFromItemId = '6')
            print(ipn+' exists')

# Validate item log existance
            if isinstance(obs, float) == False:
                print(ipn+' observations are: '+obs+'\n')
                print('Updating observations to '+ipn)

#Upload the log to the item
                id = login.getItemByUniqueAttributes('Inventory', ipn, itemIdentifier1 = sn, derivedFromItemId = '6')[u'id']
                obs = 'ATMOS: '+obs
                login.addLogEntryToItemWithItemId(id, unidecode.unidecode(obs))
                print('Update complete.\n')

            else:
                print(ipn+" doesn't have any observations\n")

        except cdb.common.exceptions.objectNotFound.ObjectNotFound:
            print(ipn+" doesn't exist. Adding to Database...")
            login.addItem('Inventory', ipn,'Sample', itemIdentifier1 = sn, derivedFromItemId = '6')
            id = login.getItemByUniqueAttributes('Inventory', ipn, itemIdentifier1 = sn, derivedFromItemId = '6')[u'id']
            print(ipn+' Uploaded to Database. Item Id is: '+id)

            if isinstance(obs, float) == False:
                print(ipn+' observations are: '+obs)
                print('Updating observations to '+ipn)

                id = login.getItemByUniqueAttributes('Inventory', ipn, itemIdentifier1 = sn, derivedFromItemId = '6')[u'id']
                obs = 'ATMOS: '+obs
                login.addLogEntryToItemWithItemId(id, unidecode.unidecode(obs))
                print('Update complete.\n')

            else:
                print(ipn+" doesn't have any observations\n")

#For AFCs Timing
    if ":3.1T:" in ipn:
        try:
            login.getItemByUniqueAttributes('Inventory', ipn, itemIdentifier1 = sn, derivedFromItemId = '78')
            print(ipn+' exists')

# Validate item log existance
            if isinstance(obs, float) == False:
                print(ipn+' observations are: '+obs+'\n')
                print('Updating observations to '+ipn)

#Upload the log to the item
                id = login.getItemByUniqueAttributes('Inventory', ipn, itemIdentifier1 = sn, derivedFromItemId = '78')[u'id']
                obs = 'ATMOS: '+obs
                login.addLogEntryToItemWithItemId(id, unidecode.unidecode(obs))
                print('Update complete.\n')

            else:
                print(ipn+" doesn't have any observations\n")

        except cdb.common.exceptions.objectNotFound.ObjectNotFound:
            print(ipn+" doesn't exist. Adding to Database...")
            login.addItem('Inventory', ipn,'Sample', itemIdentifier1 = sn, derivedFromItemId = '78')
            id = login.getItemByUniqueAttributes('Inventory', ipn, itemIdentifier1 = sn, derivedFromItemId = '78')[u'id']
            print(ipn+' Uploaded to Database. Item Id is: '+id)

            if isinstance(obs, float) == False:
                print(ipn+' observations are: '+obs)
                print('Updating observations to '+ipn)

                id = login.getItemByUniqueAttributes('Inventory', ipn, itemIdentifier1 = sn, derivedFromItemId = '78')[u'id']
                obs = 'ATMOS: '+obs
                login.addLogEntryToItemWithItemId(id, unidecode.unidecode(obs))
                print('Update complete.\n')

            else:
                print(ipn+" doesn't have any observations\n")

print('Item and item logs update complete.')
