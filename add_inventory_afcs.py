# -*- coding: utf-8 -*-
"""
Created on Tue, May 19 ‎12:14:25 2020

CDB Add Item

@author: Caio Santos - DIG
"""

from cdb.cdb_web_service.api.itemRestApi import ItemRestApi
from cdb.common.exceptions.invalidRequest import InvalidRequest
from cdb.common.exceptions.objectAlreadyExists import ObjectAlreadyExists
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import load_workbook
import pandas as pd
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

x = 0
y = 0
z = 0

for data in ws.iter_rows(values_only=True):
    if 'AFC' in data and '3.1T' not in data:
        exec("item"+str(x)+" = list(data)")
        exec("del item"+str(x)+"[0]")
        exec("name"+str(x)+" = item"+str(x)+"[0]+':3.1:'+item"+str(x)+"[1]")
        exec("print(name"+str(x)+")")

        try:
            exec("login.addItem('Inventory', name"+str(x)+",'Sample', itemIdentifier1 = item"+str(x)+"[4], description = 'Testing for final upload', derivedFromItemId = '6')")
            exec("print(item"+str(x)+"[0]+' added to Database')")
            z += 1
        except:
            exec("print(item"+str(x)+"[0]+' already exists in the Database')")
            y += 1
        x += 1

if y != 0:
    print('\n'+str(y)+' items were not uploaded to the Database.')

elif y == 0:
    print('\nAll items were uploaded successfully!')
