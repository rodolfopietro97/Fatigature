import base64
import json
import sys
import time

import rsa

from CummareApi.CummreClient import publish, subscribe
from Utils.ConfigurationFileHandler import ConfigurationFileHandler
from Utils.Constants import CONFIGURATION_FILE_PATH, MESSAGE_ENCODING

random_responses = []
"""
Random responses obtained
"""

str_public_key = ""
"""
String of public key
"""


def fetch_random_responses(random_response):
    random_response_object = json.loads(random_response)

    if random_response_object['public_key'] == str_public_key:
        encrypted_response = base64.b64decode(random_response_object['data'].encode(MESSAGE_ENCODING))
        random_number = rsa.decrypt(encrypted_response, private_key)
        random_number_string = random_number.decode(MESSAGE_ENCODING)
        random_responses.append(random_number_string)


if __name__ == '__main__':
    """
    Simple client that send transaction
    """

    # Init parameters
    cummare_server = ConfigurationFileHandler.get_generic_property(CONFIGURATION_FILE_PATH, "CummareServer")

    random_request_topic = ConfigurationFileHandler.get_generic_property(CONFIGURATION_FILE_PATH, "Topics")['random_requests']
    random_responses_topic = ConfigurationFileHandler.get_generic_property(CONFIGURATION_FILE_PATH, "Topics")['random_responses']

    queue_to_use = sys.argv[1]

    waiting_time = int(sys.argv[2])

    (public_key, private_key) = rsa.newkeys(1024)

    str_public_key = public_key.save_pkcs1("PEM").decode(MESSAGE_ENCODING)

    random_request = {
        "queue": queue_to_use,
        "public_key": str_public_key
    }

    # Send random request
    if publish(cummare_server=cummare_server, topic=random_request_topic, message=json.dumps(random_request)):
        print(f"{cummare_server} - RECEIVED")
    else:
        print(f"{cummare_server} - REJECTED")

    # Wait random response
    start = time.time()

    while (time.time() - start) <= waiting_time:
        subscribe(cummare_server=cummare_server, topic=random_responses_topic, process_function=fetch_random_responses)
        time.sleep(waiting_time / 4)

    print("\n".join(set(random_responses)))
