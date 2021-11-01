from CummareApi.CummreClient import publish, subscribe
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

    # Send transaction and wait result
    subscribe(cummare_server=cummare_server, topic=transaction_topic, process_function=print)