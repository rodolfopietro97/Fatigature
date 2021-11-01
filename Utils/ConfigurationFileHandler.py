import json
import sys

from Utils.Constants import QUEUE_DATA_TYPES, INVALID_CHARACTERS_FOR_QUEUE_NAME
from Utils.Exceptions.CasoCavalloQueuesExceptions import InvalidRangeForDataType, InvalidCasoCavalloQueueDataType, \
    InvalidCasoCavalloQueueName, InvalidRandomBytesSizeForDataTypeRandomBytes


class ConfigurationFileHandler:
    """
    Handle json configuration files.

    It uses rules of our JSON files
    """

    @staticmethod
    def load_cummare_servers_from_configuration_file(configuration_file_path: str):
        """
        Load cummare servers contained in network configuration files.

        :param configuration_file_path: Path of configuration file

        :return: Servers on configuration file
        """

        # Queues to use (empty default)
        cummare_servers = []

        try:
            # Open config.json
            config_file = json.load(open(configuration_file_path))

            # Get all queues in configuration file
            cummare_servers = [
                cummare_server
                for cummare_server in config_file['CummareServers']
            ]

        # Configuration file doesn't exists
        except FileNotFoundError as file_not_foundError:
            print(f"Error on load CasoCavallo Random Number Generator. "
                  f"Missing config file\n{file_not_foundError}", file=sys.stderr)

        # Key error on json file
        except KeyError as key_error:
            print(f"Syntax error on {configuration_file_path} Or missing a key\n{key_error}",
                  file=sys.stderr)

        # Generic error, to handle unexpected behaviors
        except Exception as exception:
            print(f"Generic Error on load CasoCavallo Random Number Generator.\n{exception}",
                  file=sys.stderr)

        # Return the random sources on configuration file
        return cummare_servers

    @staticmethod
    def load_redis_server_from_configuration_file(configuration_file_path: str):
        """
        Load Redis server contained in network configuration files.

        :param configuration_file_path: Path of configuration file

        :return: Redis server on configuration file
        """

        try:
            # Open config.json
            config_file = json.load(open(configuration_file_path))

            # Get all queues in configuration file
            redis_server = config_file['RedisServer']

        # Configuration file doesn't exists
        except FileNotFoundError as file_not_foundError:
            print(f"Error on load CasoCavallo Random Number Generator. "
                  f"Missing config file\n{file_not_foundError}", file=sys.stderr)

        # Key error on json file
        except KeyError as key_error:
            print(f"Syntax error on {configuration_file_path} Or missing a key\n{key_error}",
                  file=sys.stderr)

        # Generic error, to handle unexpected behaviors
        except Exception as exception:
            print(f"Generic Error on load CasoCavallo Random Number Generator.\n{exception}",
                  file=sys.stderr)

        # Return the random sources on configuration file
        return redis_server

    @staticmethod
    def get_generic_property(configuration_file_path: str, property_in_configuration_file: str):
        """
        Get generic property in configuration file

        :param configuration_file_path: Path of configuration file
        :param property_in_configuration_file: Property name in configuration file

        :return: Property value
        """

        try:
            # Open config.json
            config_file = json.load(open(configuration_file_path))

            # Get all queues in configuration file
            property_value = config_file[property_in_configuration_file]

        # Configuration file doesn't exists
        except FileNotFoundError as file_not_foundError:
            print(f"Error on load Configuration File. "
                  f"Missing config file\n{file_not_foundError}", file=sys.stderr)

        # Key error on json file
        except KeyError as key_error:
            print(f"Syntax error on {configuration_file_path} Or missing a key\n{key_error}",
                  file=sys.stderr)

        # Generic error, to handle unexpected behaviors
        except Exception as exception:
            print(f"Generic Error on load property form configuration file.\n{exception}",
                  file=sys.stderr)

        # Return the value of property
        return property_value


    @staticmethod
    def load_queues_from_configuration_file(configuration_file_path: str):
        """
        Load random queues contained in configuration files.

        THis method is very important because set correct random queues
        by using parameters

        :param configuration_file_path: Path of configuration file

        :return: Queues on configuration file
        """

        # Queues to use (empty default)
        queues = []

        try:
            # Open config.json
            config_file = json.load(open(configuration_file_path))

            # Get all queues in configuration file
            queues = [
                queue
                for queue in config_file['CasoCavalloQueues']

                # Only valid queues
                if ConfigurationFileHandler.is_valid_queue(queue)
            ]

        # Configuration file doesn't exists
        except FileNotFoundError as file_not_foundError:
            print(f"Error on load CasoCavallo Random Number Generator. "
                  f"Missing config file\n{file_not_foundError}", file=sys.stderr)

        # Key error on json file
        except KeyError as key_error:
            print(f"Syntax error on {configuration_file_path} Or missing a key\n{key_error}",
                  file=sys.stderr)

        # Invalid queue name -> Queue contains invalid characters
        except InvalidCasoCavalloQueueName as invalid_queue_name:
            print(f"Error on queue names. There is an incorrect name.\n{invalid_queue_name}",
                  file=sys.stderr)

        # Invalid queue data type -> Datatype wrong
        except InvalidCasoCavalloQueueDataType as invalid_queue_data_type:
            print(f"Error on queue data types. There is an incorrect data type.\n{invalid_queue_data_type}",
                  file=sys.stderr)

        # Invalid queue data type -> Random bytes size of queue is invalid
        except InvalidRandomBytesSizeForDataTypeRandomBytes as invalid_random_bytes_size:
            print(f"Error on queue size. Incorrect random bytes size.\n{invalid_random_bytes_size}",
                  file=sys.stderr)

        # Invalid queue data type-> Invalid size of range of queue
        except InvalidRangeForDataType as invalid_random_bytes_size:
            print(f"Error on queue range. Incorrect range for data type INTEGER or REAL.\n{invalid_random_bytes_size}",
                  file=sys.stderr)

        # Generic error, to handle unexpected behaviors
        except Exception as exception:
            print(f"Error on load CasoCavallo Random Number Generator.\n{exception}",
                  file=sys.stderr)

        # Return the random sources on configuration file
        return queues

    @staticmethod
    def is_valid_queue(queue_to_analyze: dict):
        """
        Validate the syntax of a queue.

        For example:
        * A BINARY queue cannot have size
        * Data types of queue must be established
        * ...

        :param queue_to_analyze: Queue to parse/analyze

        :return: True if a queue is valid, False otherwise
        """

        # Name cannot contains invalid characters
        for invalid_character in INVALID_CHARACTERS_FOR_QUEUE_NAME:
            if invalid_character in queue_to_analyze['name']:
                raise InvalidCasoCavalloQueueName()

        # Check data type
        if queue_to_analyze['type'] not in QUEUE_DATA_TYPES:
            raise InvalidCasoCavalloQueueDataType()

        # Random bytes must have a size greater than 0
        if queue_to_analyze['type'] == "RANDOM_BYTES":
            if queue_to_analyze['size'] is None \
                    or \
                    not isinstance(queue_to_analyze['size'], int) \
                    or \
                    int(queue_to_analyze['size']) <= 0:
                raise InvalidRandomBytesSizeForDataTypeRandomBytes()

        # Reals must have a range
        if queue_to_analyze['type'] == "REAL":
            if len(queue_to_analyze['range']) != 2 \
                    or \
                    not (isinstance(queue_to_analyze['range'][0], float) or isinstance(queue_to_analyze['range'][0], int)) \
                    or \
                    not (isinstance(queue_to_analyze['range'][1], float) or isinstance(queue_to_analyze['range'][1], int)) \
                    or \
                    queue_to_analyze['range'][1] <= queue_to_analyze['range'][0]:
                raise InvalidRangeForDataType()

        # Integers must have a correct range
        if queue_to_analyze['type'] == "INTEGER":
            if len(queue_to_analyze['range']) != 2 \
                    or \
                    not isinstance(queue_to_analyze['range'][0], int) \
                    or \
                    not isinstance(queue_to_analyze['range'][1], int) \
                    or \
                    queue_to_analyze['range'][1] <= queue_to_analyze['range'][0]:
                raise InvalidRangeForDataType()

        # All validations are passed
        return True
