import json
from functools import reduce
from time import sleep

from CummareApi.CummreClient import subscribe, publish
from Mining.ProofOfLottery import ProofOfLottery
from Utils.ConfigurationFileHandler import ConfigurationFileHandler
from Utils.Constants import CONFIGURATION_FILE_PATH, BOSS_CONFIGURATION_FILE_PATH

my_lotteries = {}

last_lottery = -1

new_lottery_is_started = True

random_number = (0, 0)

my_message_was_deleted = True

HEX_ALPHABET = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
"""
Alphabet of hexadecimal numbers
"""


def handle_current_lottery_id(current_lottery):
    global random_number
    global my_lotteries

    current_lottery_object = json.loads(current_lottery.strip())
    lottery_id = current_lottery_object['lottery_id']

    if lottery_id not in my_lotteries:
        temp_random_lottery = {
            "random_number": random_number[0],
            "lottery_id": lottery_id,
            "random_verifier": random_number[1]
        }
        my_lotteries[lottery_id] = temp_random_lottery


def check_my_message(current_lottery):
    global my_message_was_deleted
    global last_lottery

    current_lottery_object = json.loads(current_lottery.strip())

    if current_lottery_object["random_number"] == my_lotteries[last_lottery]["random_number"]:
        my_message_was_deleted = False


if __name__ == '__main__':
    """
    Real time server.
    Every asks pending transactions

    :param cummare_server: Address of Cummare Server
    """
    # Init parameters
    cummare_server = ConfigurationFileHandler.get_generic_property(CONFIGURATION_FILE_PATH, "CummareServer")

    round_duration = int(ConfigurationFileHandler.get_generic_property(BOSS_CONFIGURATION_FILE_PATH, "roundDuration"))

    while True:

        # 1) Fetch current lottery id
        subscribe(cummare_server=cummare_server, topic="current_lottery", process_function=handle_current_lottery_id)

        # 2) Generate random for current lottery id
        if len(my_lotteries.keys()) > 0:
            new_lottery = max(list(my_lotteries.keys()))
            if new_lottery != last_lottery:
                last_lottery = new_lottery

                random_number = ProofOfLottery.generate_winning_numbers("boss")

            my_message_was_deleted = True
            subscribe(cummare_server=cummare_server, topic="boss_lotteries", process_function=check_my_message)

            if my_message_was_deleted:
                publish(cummare_server=cummare_server,
                        topic="boss_lotteries",
                        message=str(json.dumps(my_lotteries[last_lottery])))

            sleep(round_duration/10)
