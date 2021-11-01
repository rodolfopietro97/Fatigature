import random
from time import sleep

from CummareApi.CummreClient import publish
from Utils.ConfigurationFileHandler import ConfigurationFileHandler
from Utils.Constants import CONFIGURATION_FILE_PATH

import sys

import json

if __name__ == '__main__':
    """
    Simple client that send transaction
    """

    # Init parameters
    cummare_server = ConfigurationFileHandler.get_generic_property(CONFIGURATION_FILE_PATH, "CummareServer")

    transaction_topic = ConfigurationFileHandler.get_generic_property(CONFIGURATION_FILE_PATH, "Topics")['transaction']

    transaction = {
        "from": sys.argv[1],
        "to": sys.argv[2],
        "amount": sys.argv[3]
    }

    while True:
        # Send transaction and wait result
        transaction['amount'] = random.randint(0, 100000)
        if publish(cummare_server=cummare_server, topic=transaction_topic, message=json.dumps(transaction)):
            print(f"{cummare_server} - RECEIVED")
        else:
            print(f"{cummare_server} - REJECTED")
        sleep(0.1)