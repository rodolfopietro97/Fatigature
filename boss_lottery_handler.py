import time
from time import sleep

from CummareApi.CummreClient import subscribe, publish
from Mining.ProofOfLottery import ProofOfLottery

import json

from Utils.ConfigurationFileHandler import ConfigurationFileHandler
from Utils.Constants import CONFIGURATION_FILE_PATH, BOSS_CONFIGURATION_FILE_PATH

current_round_must_update = False
"""
Say if current round must update
"""

# Init parameters
cummare_server = ConfigurationFileHandler.get_generic_property(CONFIGURATION_FILE_PATH, "CummareServer")

current_lottery = {
    "lottery_id": 0,
}
"""
Init current lottery
"""


def update_lottery(current):
    """
    Push pending transactions

    :param pending_transaction: Random request to push
    """
    global current_round_must_update

    if current:
        current_round_must_update = False


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
        # 1) Generate current lottery id
        current_lottery['lottery_id'] = current_lottery['lottery_id'] + 1

        # 2) take it for 2 seconds
        start = time.time()
        publish(cummare_server=cummare_server, topic="current_lottery", message=str(json.dumps(current_lottery)))

        while (time.time() - start) <= round_duration:
            current_round_must_update = True

            subscribe(cummare_server=cummare_server, topic="current_lottery", process_function=update_lottery)

            if current_round_must_update:
                publish(cummare_server=cummare_server,
                        topic="current_lottery",
                        message=str(json.dumps(current_lottery)))

            sleep(round_duration/10)
