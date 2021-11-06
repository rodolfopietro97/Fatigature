CONFIGURATION_FILE_PATH = "../Configurations/FatigatureConfig.json"
"""
Path of configuration file.

Configuration file contains informations
"""


CASOCAVALLO_CONFIGURATION_FILE_PATH = "../Configurations/CasoCavalloConfig.json"
"""
Path of configuration file of CasoCavallo.

Configuration file contains informations of CasoCavallo
"""


BOSS_CONFIGURATION_FILE_PATH = "../Configurations/BossConfig.json"
"""
Path of configuration file of CasoCavallo.

Configuration file contains informations of CasoCavallo
"""



MESSAGE_ENCODING = 'ISO-8859-1'
"""
Encoding format for messages
(Useful to avoid problem with python rsa)
"""


INVALID_CHARACTERS_FOR_QUEUE_NAME = [" "]
"""
Invalid characters for a queue name
"""


QUEUE_DATA_TYPES = [
    "BINARY",
    "RANDOM_BYTES",
    "REAL",
    "INTEGER"
]
"""
Data types for random queues
"""