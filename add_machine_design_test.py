# -*- coding: utf-8 -*-
"""
Created on Fri, Jun 31 ‎13:19:40 2020

CDB Add Machine Design

@author: Caio Santos - DIG
"""

from cdb.cdb_web_service.api.itemRestApi import ItemRestApi
from cdb.common.exceptions.invalidRequest import InvalidRequest
from cdb.common.exceptions.objectAlreadyExists import ObjectAlreadyExists
import openpyxl
import getpass

print('Logging into CDB...')
#Reads the credentials and save in the variables to connect to the server
protocol = raw_input("\nNetwork protocol: ")
server = raw_input("CDB server: ")
port = int(input("Server port: "))
user = raw_input("CDB user name: ")
password = getpass.getpass(prompt = "Password: ")

#Log into CDB database
login = ItemRestApi(user, password, server, port, protocol)
print('Login successfully.\n\nReading worksheet...\n')

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

#Add Racks in CDB with name, label and description
for x in range(0, 22):
    r_name = ''
    if 'TL' in MC['Rack'][x]:
        r_name = 'BPM Rack 20-TL'
        description = 'Rack for Beam Position Monitoring system in transport line'
        print('Adding %s to Database...' % (r_name))
        login.addItem('Machine Design', r_name, 'Sample', MC['Rack'][x], description = description)
        print('%s added successfully!\n' % (r_name))

    elif 'Spare' in MC['Rack'][x]:
        r_name = 'BPM Homolog Rack'
        description = 'Homolog Rack for Beam Position Monitoring system'
        print('Adding Rack %s to Database...' % (r_name))
        login.addItem('Machine Design', r_name, 'Sample', MC['Rack'][x], description = description)
        print('%s added successfully!\n' % (r_name))

    else:
        r_name = 'BPM Rack '+str(MC['Rack'][x][3:5])
        description = 'Rack for Beam Position Monitoring system'
        print('Adding Rack %s to Database...' % (r_name))
        login.addItem('Machine Design', r_name, 'Sample', MC['Rack'][x], description = description)
        print('%s added successfully!\n' % (r_name))

#Add Crate uTCA Placeholders in CDB with name, label and description
for x in range(0, 22):
    c_name = ''
    if 'TL' in MC['Crate'][x]:
        c_name = 'Rack 20-TL MicroTCA Crate'
        description = 'Crate MicroTCA for Rack 20-TL'
        print('Adding %s to Database...' % (c_name))
        login.addItem('Machine Design', c_name, 'Sample', MC['Rack'][x], description = description)
        print('%s added successfully!\n' % (c_name))

    elif 'BPM:' in MC['Crate'][x]:
        c_name = 'Rack '+str(MC['Crate'][x][3:5])+' MicroTCA Crate'
        description = 'Crate MicroTCA for Rack '+str(MC['Crate'][x][3:5])
        print('Adding %s to Database...' % (c_name))
        login.addItem('Machine Design', c_name, 'Sample', MC['Rack'][x], description = description)
        print('%s added successfully!\n' % (c_name))

    elif 'BPM:' not in MC['Crate'][x] or 'TL' not in MC['Crate'][x]:
        c_name = 'Homolog Rack MicroTCA Crate'
        description = 'Crate MicroTCA for Homolog Rack'
        print('Adding %s to Database...' % (c_name))
        login.addItem('Machine Design', c_name, 'Sample', MC['Rack'][x], description = description)
        print('%s added successfully!\n' % (c_name))

#Add Crates as Contained Items for Racks as Parent Items
for x in range(0, 22):
    print('Adding '+MC['Crate'][x]+' as parent of '+MC['Rack'][x]+'...')
    addItemElement('component', MC['Rack'][x], MC['Crate'][x])
    print('Hierarchy added successfully!\n')
