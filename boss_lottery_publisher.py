from time import sleep

from CummareApi.CummreClient import subscribe, publish
from Mining.ProofOfLottery import ProofOfLottery

import json

from Utils.ConfigurationFileHandler import ConfigurationFileHandler
from Utils.Constants import CONFIGURATION_FILE_PATH


# boss_lotteries = []
#
# current_lottery_id = -1
#
# a_new_lottery_is_started = False

my_lotteries = {}

last_lottery = -1


def handle_current_lottery_id(current_lottery):
    current_lottery_object = json.loads(current_lottery.strip())
    lottery_id = current_lottery_object['lottery_id']

    if lottery_id not in my_lotteries:
        temp_random_number = ProofOfLottery.generate_winning_numbers("boss")
        temp_random_lottery = {
            "random_number": temp_random_number[0],
            "random_verifier": temp_random_number[1],
            "lottery_id": lottery_id
        }
        my_lotteries[lottery_id] = temp_random_lottery


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
        subscribe(cummare_server=cummare_server, topic="current_lottery", process_function=handle_current_lottery_id)

        # 2) Publish lottery if not published
        new_lottery = max(list(my_lotteries.keys()))
        if new_lottery != last_lottery:
            last_lottery = new_lottery
            publish(cummare_server=cummare_server, topic="boss_lotteries", message=str(json.dumps(my_lotteries[last_lottery])))
        # A new lottery process is started
        # if a_new_lottery_is_started:
        #     a_new_lottery_is_started = False
        #
        #     # 2) Generate lottery number
        #     random_number = ProofOfLottery.generate_winning_numbers("boss")
        #     random_lottery = {
        #         "random_number": random_number[0],
        #         "random_verifier": random_number[1],
        #         "lottery_id": current_lottery_id
        #     }
        #
        #     # Publish and append my number
        #     publish(cummare_server=cummare_server, topic="boss_lottery", message=str(json.dumps(random_lottery)))
        #
        # else:
        #     print("weee")

        sleep(0.1)
        # boss_lotteries.append(random_number[0])
        #
        # # 2) Fetch lottery number of other bosses
        # subscribe(cummare_server=cummare_server, topic="boss_lottery", process_function=lottery_round)
        #
        # # 3) Sleep 2 seconds before confirm winner (and in this time find less distant
        # # sleep(2)
        # print(boss_lotteries)
        # print("")
        #
        # # 4) Clear number for round
        # boss_lotteries.clear()


        # # 1) Fetch transactions and push new blocks in block mining requests
        #
        # # Subscribe and add transactions
        # subscribe(cummare_server=cummare_server, topic="transaction", process_function=push_pending_transaction)
        #
        # blocks_count = 0
        #
        # # If we have more than 1 transaction
        # if len(pending_transactions) > 1:
        #
        #     # Create new block
        #     new_block = ProofOfLottery.calculate(
        #         miner_address="miner",
        #         received_transactions=[json.loads(transaction) for transaction in pending_transactions]
        #     )
        #
        #     # Push new block
        #     publish(cummare_server=cummare_server, topic="block_mining_requests", message=str(json.dumps(new_block)))
        #
        #     # Delete pending transactions
        #     pending_transactions.clear()
        #
        # # 2) Wait response
