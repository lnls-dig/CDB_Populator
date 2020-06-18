# -*- coding: utf-8 -*-
"""
Created on Tue, May 12 ‎16:33:53 2020

ComponentDB Domain Names Receiver

@author: Caio Santos - DIG
"""

from cdb.cdb_web_service.api.itemRestApi import ItemRestApi
from cdb.common.exceptions.invalidRequest import InvalidRequest
import pandas as pd
import getpass
from collections import OrderedDict

#Set the maximum columns width
pd.set_option('max_colwidth', 80)

print("\n\n"+"**"*17+" CDB DOMAIN NAMES "+"**"*17+"\n\nINSERT CDB CREDENTIALS")

#Reads the credentials and save in the variables to connect to the server
#Reads the credentials and save in the variables to connect to the server
protocol = raw_input("\nNetwork protocol: ")
server = raw_input("CDB server: ")
port = int(input("Server port: "))
user = raw_input("CDB user name: ")
password = getpass.getpass(prompt = "Password: ")

#Log into CDB database
login = ItemRestApi(user, password, server, port, protocol)
domain = login.getDomains()

w = 'dom'
x = 0
y = 'item'
z = 0
dom_list = []

#Formats the data received from CDB into easier interpretation dictionaries
for item in domain :
    exec(w+str(x)+'= domain[x]')
    exec("if u'item_category_label' in "+ w+str(x)+ ": del "+ w+str(x) +"[u'item_category_label']")
    exec("if u'item_identifier1_label' in "+ w+str(x)+ ": del "+ w+str(x) +"[u'item_identifier1_label']")
    exec("if u'item_identifier2_label' in "+ w+str(x)+ ": del "+ w+str(x) +"[u'item_identifier2_label']")
    exec("if u'item_type_label' in "+ w+str(x)+ ": del "+ w+str(x) +"[u'item_type_label']")
    exec(y+str(z)+'=OrderedDict(sorted('+w+str(x)+'.items(), reverse=True))')
    exec("dom_list.append("+y+str(z)+".values())") #Add ordered dictionaries values into a list
    x += 1
    z += 1

#Creates a DataFrame with the lists values
dom_table = pd.DataFrame(dom_list, columns = ['Domain ID', 'Domain Name', 'Domain Description'])

print("**"*17+" DOMAIN NAMES LIST "+"**"*17+"\n")
print(dom_table)
