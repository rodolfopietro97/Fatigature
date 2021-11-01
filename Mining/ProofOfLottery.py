from datetime import datetime
import hashlib
import random
import sys

import json


class ProofOfLottery:
    """
    Implementation of proof of lottery
    with validation.
    Useful in two sides:
        When miner do proof of lottery
        When miner approve the proof of lottery of other miners
    """

    @staticmethod
    def stringifyTransactionList(transactions_list):
        """
        Stringify a list of transaction

        :param transactions_list: Transaction list to stringify
        :return: String encoding of transactions

        @TODO: improve or remove

        """

        return json.dumps(transactions_list)

    # @staticmethod
    # def deStringifyTransactionString(transactionListAsString):
    #     """
    #     Transform a string (that express a list of transactions)
    #     in a list of TransactionObject.
    #
    #     It is useful because permit us to make simmetric difference
    #     with respect to transactions we have.
    #     Is possible in fact that a miner can mine before us a transactions
    #     that we need to mine
    #
    #     :param transactionListAsString: List of transactions expressed as string
    #
    #     :return: List of TransactionObject
    #
    #     @TODO: improve or remove
    #     """
    #
    #     json.loads(transactionListAsString)

    @staticmethod
    def lottery(hash_string):
        """
        Calculate lottery function over a hash string

        :param hash_string: Hash over calculate lottery function

        :return: Lottery number
        """

        # Sum all
        return sum(
            # List all
            list(map(ord, hash_string))
        )

    @staticmethod
    def verify(block):
        """
        Verify if block is validate correctly by a miner
        (BLOCK VERIFICATION)

        :param block: Block to verify

        :return: True if yes, False if not

        """

        # Lottery is correct the same on hashed miner address and on lotteryFunctionBlockHash
        correct_lottery = (ProofOfLottery.lottery(block['hashed_miner_address']) == int(block['lottery_number']))

        # Correct calculated block hash
        received_transactions_concat_nonce = json.dumps(block['transactions']) + block['nonce']
        correct_block_hash = (block['block_hash'] == hashlib.sha256(str.encode(received_transactions_concat_nonce)).hexdigest())

        # Return final verify
        return correct_lottery and correct_block_hash

    @staticmethod
    def verify_winning_number_of_block(miner_address, block):
        """
        Verify the winning number of a block
        (WINNER VERIFICATION)

        :param miner_address: Address of miner
        :param block: Block to verify

        :return: Correct or incorrect verification
        """
        return block['winning_number_verifier'] == hashlib.sha256(str.encode(miner_address + block['winning_number'])).hexdigest()

    @staticmethod
    def generate_winning_numbers(miner_address):
        # Set hex alphabet
        hex_alphabet = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

        # Set winning and verification number
        winning_number = "".join([hex_alphabet[random.randint(0, len(hex_alphabet)-1)] for index in range(32)])
        verification_winning_number = hashlib.sha256(str.encode(miner_address + winning_number)).hexdigest()

        # Return lottery winning numbers
        return winning_number, verification_winning_number

    @staticmethod
    def calculate(miner_address, received_transactions):
        """
        Calculate Proof Of Lottery

        :param miner_address: Address of miner who do the proof of lottery
        :param received_transactions: List of received received

        :return:
        """

        # hashed miner address
        hashed_miner_address = hashlib.sha256(str.encode(miner_address)).hexdigest()

        # Lottery function over miner
        lottery_function_on_miner_address = ProofOfLottery.lottery(hashed_miner_address)

        # Stringify transactions
        received_transactions_stringify = ProofOfLottery.stringifyTransactionList(received_transactions)

        # Main loop
        find_correct_seed = False
        seed = 0
        while not find_correct_seed:
            # Update seed RANDOMLY
            seed = random.randint(0, sys.maxsize)

            # Concatenate received transaction string with seed
            stringify_seed = str(seed)
            received_transactions_concat_seed = received_transactions_stringify + stringify_seed

            # Try to construct block hash using seed and transactions
            block_hash = hashlib.sha256(str.encode(received_transactions_concat_seed)).hexdigest()

            # Condition of winning
            lottery_function_block_hash = ProofOfLottery.lottery(block_hash)
            if lottery_function_block_hash == lottery_function_on_miner_address:
                find_correct_seed = True

        # When block is mined
        current_date_time = datetime.now().strftime("%d/%m/%Y,%H:%M:%S")

        # Generate lottery winning numbers
        winning_number = ProofOfLottery.generate_winning_numbers(miner_address=miner_address)
        # winning_number = (10, 20)

        # Create block object
        block = {
            "creation_timestamp": current_date_time,
            "nonce": stringify_seed,
            "transactions": json.loads(received_transactions_stringify),
            "block_hash": block_hash,
            "lottery_number": lottery_function_block_hash,
            "hashed_miner_address": hashed_miner_address,
            "winning_number": winning_number[0],
            "winning_number_verifier": winning_number[1]
        }

        # Return useful data to create new block
        return block
