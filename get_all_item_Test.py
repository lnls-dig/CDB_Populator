from cdb.cdb_web_service.api.itemRestApi import ItemRestApi
from cdb.common.exceptions.invalidRequest import InvalidRequest

#Reads a file with the credentials and save in the "line" variables
data = open('account_cdb.txt', 'r')
line = data.readlines()
user = line[0]
password = line[1]
server = line[2]
port = 10232
protocol = line[4]
data.close

login = ItemRestApi(user, password, server, port, protocol)
item = login.getCatalogItems()

print(item)
