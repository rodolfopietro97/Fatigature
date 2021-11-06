import json
import sys

import rsa

from CummareApi.CummreClient import publish, subscribe
from Utils.ConfigurationFileHandler import ConfigurationFileHandler
from Utils.Constants import CONFIGURATION_FILE_PATH, MESSAGE_ENCODING, CASOCAVALLO_CONFIGURATION_FILE_PATH

import time

from time import sleep

import redis

import base64

import sys

random_requests = {}
"""
Random requests to solve
"""


def push_random_requests(random_request):
    """
    Solve random requests

    :param random_request: Random request to solve
    """

    # Remove timestamp form request
    random_request_without_timestamp = json.loads(random_request.strip())
    del random_request_without_timestamp['timestamp']

    random_request_without_timestamp_as_string = json.dumps(random_request_without_timestamp)

    # Add to requests if not exists
    if random_request_without_timestamp_as_string not in random_requests:
        # Set as not solved
        random_requests[random_request_without_timestamp_as_string] = int(sys.argv[1])


if __name__ == '__main__':
    """
    Simple client that send transaction
    """

    # Init parameters
    cummare_server = ConfigurationFileHandler.get_generic_property(CONFIGURATION_FILE_PATH, "CummareServer")

    random_request_topic = ConfigurationFileHandler.get_generic_property(CONFIGURATION_FILE_PATH, "Topics")['random_requests']
    random_responses_topic = ConfigurationFileHandler.get_generic_property(CONFIGURATION_FILE_PATH, "Topics")['random_responses']

    # For each redis list init currents random numbers
    currents_randoms = {}

    # Init redis client
    redis_server = ConfigurationFileHandler.load_redis_server_from_configuration_file(CASOCAVALLO_CONFIGURATION_FILE_PATH)
    redis_client = redis.Redis(
        host=redis_server['host'],
        port=redis_server['port'],
        db=redis_server['database'],
        socket_timeout=redis_server['connection_timeout']
    )

    # Load all redis queues from configuration file
    redis_queues = ConfigurationFileHandler \
        .load_queues_from_configuration_file(CASOCAVALLO_CONFIGURATION_FILE_PATH)

    # Get redis lists names from our redis queues
    redis_lists = [redis_queue['name'] for redis_queue in redis_queues]

    # Run forever
    while True:

        # Update currents randoms
        for queue in redis_lists:
            currents_randoms[queue] = redis_client.get(f'current_{queue}').decode()

        # Create command and execute it
        subscribe(cummare_server=cummare_server,
                  topic=random_request_topic,
                  process_function=push_random_requests)

        # Solve all requests
        for random_request in random_requests:

            # Object version of request
            random_request_object = json.loads(random_request)

            # Not solved
            if random_requests[random_request] > 0:

                # If queue is valid
                if random_request_object['queue'] in redis_lists:

                    # Get public key
                    encryption_public_key = rsa.PublicKey.load_pkcs1(random_request_object['public_key'].encode(MESSAGE_ENCODING), format='PEM')

                    # Encode message
                    message_to_send_in_bytes = str(
                        currents_randoms[
                            random_request_object['queue']
                        ]
                    ).encode(MESSAGE_ENCODING)

                    # Encrypt message
                    encrypt_message = rsa.encrypt(message_to_send_in_bytes, encryption_public_key)
                    encrypt_message_string = encrypt_message.decode(MESSAGE_ENCODING)

                    # Init data on random response
                    random_response_solved = random_request_object
                    random_response_solved['data'] = base64.b64encode(encrypt_message_string.encode(MESSAGE_ENCODING)).decode()

                    # Set request as solved
                    random_requests[random_request] = random_requests[random_request] - 1

                    # Send response
                    publish(cummare_server=cummare_server, topic=random_responses_topic, message=str(json.dumps(random_response_solved)))

        sleep(0.1)
