"""
Main exceptions related to queues.
"""


class InvalidCasoCavalloQueueName(Exception):
    """
    Exception launched when a CasoCavallo Random queue
    has an invalid queue name
    """

    pass


class InvalidCasoCavalloQueueDataType(Exception):
    """
    Exception launched when a CasoCavallo Random queue
    has an invalid data type
    """

    pass


class InvalidRandomBytesSizeForDataTypeRandomBytes(Exception):
    """
    Exception launched when a CasoCavallo Random queue
    has a RANDOM_BYTES data type, but size is invalid
    """

    pass


class InvalidRangeForDataType(Exception):
    """
    Exception launched when a CasoCavallo Random queue
    has an invalid range for data types INTEGER and REAL
    """

    pass
