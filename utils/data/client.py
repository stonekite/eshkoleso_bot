import logging
import certifi
from pymongo import MongoClient
from utils.keys import connection_string

ca_file = certifi.where()

client = MongoClient(connection_string, tlsCAFile=ca_file)

try:
    print(client.server_info().get("version"))
    logging.info(client.server_info())
    client = client.eshkoleso.user_data
except Exception as exception:
    logging.critical(exception)
    quit()
