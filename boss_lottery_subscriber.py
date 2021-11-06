import json
from functools import reduce
from time import sleep

from CummareApi.CummreClient import subscribe, publish
from Mining.ProofOfLottery import ProofOfLottery
from Utils.ConfigurationFileHandler import ConfigurationFileHandler
from Utils.Constants import CONFIGURATION_FILE_PATH

import numpy as np

current_lottery = 0
current_lotteries = []

current_boss_lotteries = []

HEX_ALPHABET = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
"""
Alphabet of hexadecimal numbers
"""


def bytes_xor(bytes1: str, bytes2: str):
    """
    Make xor between two bytes expressed as string

    :param bytes1: Random bytes 1
    :param bytes2: Random bytes 2
    :return: Xor by bytes1 and bytes2
    """

    # Bytes must have same size
    assert len(bytes1) == len(bytes2)

    # Get indices (in our case number) of every alphabet symbols.
    # Every index correspond to a character: Index 0->'0', ... , Index 15->'f'
    # With one to one correspondence we make xor on indexes
    indices_bytes1 = np.array(
        [HEX_ALPHABET.index(element)
         for element in bytes1]
    )

    indices_bytes2 = np.array(
        [HEX_ALPHABET.index(element)
         for element in bytes2]
    )

    # Make xor of numbers
    indices_xor = indices_bytes1 ^ indices_bytes2

    # Return for each index the corresponding character. ALl as a string
    return ''.join(
        [
            HEX_ALPHABET[index]
            for index in np.nditer(indices_xor)
        ]
    )


def update_lottery(lottery):
    lottery_object = json.loads(lottery)

    global current_lottery
    global current_lotteries

    current_lotteries.append(lottery_object["lottery_id"])


def analyze_lotteries(lottery):
    lottery_object = json.loads(lottery)

    global current_lottery
    global current_boss_lotteries

    if lottery_object["lottery_id"] == current_lottery:
        current_boss_lotteries.append(lottery_object["random_number"])


if __name__ == '__main__':
    """
    Real time server.
    Every asks pending transactions

    :param cummare_server: Address of Cummare Server
    """
    # Init parameters
    cummare_server = ConfigurationFileHandler.get_generic_property(CONFIGURATION_FILE_PATH, "CummareServer")

    while True:

        # 1) Fetch current lottery id
        subscribe(cummare_server=cummare_server, topic="current_lottery", process_function=update_lottery)
        current_lottery = max(current_lotteries)

        # 2) Calculate xor of lotteries of current lottery and publish it after 2 seconds
        subscribe(cummare_server=cummare_server, topic="boss_lotteries", process_function=analyze_lotteries)

        if len(current_boss_lotteries) > 0:
            current_boss_lotteries = sorted(current_boss_lotteries)
            print(current_boss_lotteries)

            winner = {

            }
            print(f"Lottery: {current_lottery} Winner number: {reduce(bytes_xor, current_boss_lotteries)}")

        current_boss_lotteries.clear()
        sleep(1)
