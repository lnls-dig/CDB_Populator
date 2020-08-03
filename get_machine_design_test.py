# -*- coding: utf-8 -*-
"""
Created on Mon, Aug 12 ‎15:09:38 2020

ComponentDB Machine Design Names Receiver

@author: Caio Santos - DIG
"""

import cdb
from cdb.cdb_web_service.api.itemRestApi import ItemRestApi
from cdb.common.exceptions.invalidRequest import InvalidRequest
import openpyxl
import getpass

#Set the maximum columns width
pd.set_option('max_colwidth', 80)
print("\n\n"+"**"*17+" CDB MACHINE DESIGN NAMES "+"**"*17+"\n\nINSERT CDB CREDENTIALS")

#Reads the credentials and save in the variables to connect to the server
protocol = raw_input("\nNetwork protocol: ")
server = raw_input("CDB server: ")
port = int(input("Server port: "))
user = raw_input("CDB user name: ")
password = getpass.getpass(prompt = "Password: ")

#Log into CDB database
login = ItemRestApi(user, password, server, port, protocol)

#Reads the Excel workbook with the data
wb = openpyxl.load_workbook('config_ebpm_total.xlsx')
mc = wb['Rack montado']

#Empty dictionary to save the data
MC = {'Rack' : [],
      'Crate': [],
      'Ring': [],
      'Booster': [],
      'Transp': [],
      'Switch': [],
      'Parts': []}

#Data parsing and categorical separation
for i in range(2, 1450):
    cell = mc.cell(i, 10).value
    if cell == None:
        continue
    elif 'IN-Rack' in cell or 'Rack Spare' in cell:
        MC['Rack'].append(cell)

    elif 'SI-' in cell:
        MC['Ring'].append(cell)

    elif 'BO-' in cell:
        MC['Booster'].append(cell)

    elif 'TB-' in cell or 'TS-' in cell:
        MC['Transp'].append(cell)

    elif 'CO-Net' in cell:
        MC['Switch'].append(cell)

    elif 'DI-MTCA' in cell:
        MC['Crate'].append(cell)

    else:
        MC['Parts'].append(cell)

for i in range(0, 22):
    item = login.getItemByUniqueAttributes('Machine Design', MC['Rack'][i])
    print(item[u'name', u'itemIdentifier_1'])
