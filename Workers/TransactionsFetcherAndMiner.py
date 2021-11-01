import json

import os

from CummareApi.CummreClient import subscribe, publish
from Mining.ProofOfLottery import ProofOfLottery

pending_transactions = []
"""
List of pending transactions (we suppose all are valid)
"""


def push_pending_transaction(pending_transaction):
    """
    Push pending transactions

    :param pending_transaction: Random request to push
    """

    # Remove timestamp form request
    pending_transaction_without_timestamp = json.loads(pending_transaction.strip())
    del pending_transaction_without_timestamp['timestamp']

    pending_transaction_without_timestamp_as_string = json.dumps(pending_transaction_without_timestamp)

    # Add to requests if not exists
    if pending_transaction_without_timestamp_as_string not in pending_transactions:
        # Set as not mined
        pending_transactions.append(pending_transaction_without_timestamp_as_string)


def transaction_fetcher_worker(cummare_server):
    """
    Real time server.
    Every asks pending transactions

    :param cummare_server: Address of Cummare Server
    """

    # Subscribe and add transactions
    subscribe(cummare_server=cummare_server, topic="transaction", process_function=push_pending_transaction)

    blocks_count = 0

    # If we have more than 1 transaction
    if len(pending_transactions) > 1:

        # Create new block
        new_block = ProofOfLottery.calculate(
            miner_address="miner",
            received_transactions=[json.loads(transaction) for transaction in pending_transactions]
        )

        # Push new block
        publish(cummare_server=cummare_server, topic="block_mining_requests", message=str(json.dumps(new_block)))

        # Delete pending transactions
        pending_transactions.clear()