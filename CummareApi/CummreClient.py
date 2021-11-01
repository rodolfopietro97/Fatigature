import grpc

from CummareApi.Clients import Publish_pb2_grpc, Publish_pb2, Subscribe_pb2, Subscribe_pb2_grpc


def publish(cummare_server, topic, message):
    """
    Simple publish client

    :param cummare_server: Cummare server address
    :param topic: Topic where publish
    :param message: Message to publish

    :return: If message is published or not
    """

    # Create request
    request = Publish_pb2.PublishRequest(topic=topic, message=message)

    # Send request
    with grpc.insecure_channel(cummare_server) as channel:
        client = Publish_pb2_grpc.PublishTopicStub(channel)
        response = client.publishMessage(request)

    # Return response
    return response.ack


def subscribe(cummare_server, topic, process_function):
    """
    Simple subscribe client

    :param cummare_server: Cummare server address
    :param topic: Topic where publish
    :param process_function: Function to use over responses

    :return: List of messages of topic
    """

    # Create request
    request = Subscribe_pb2.SubscribeRequest(topic=topic)

    # Responses
    responses = []

    # Send request
    with grpc.insecure_channel(cummare_server) as channel:
        client = Subscribe_pb2_grpc.SubscribeTopicStub(channel)

        for response in client.subscribeTopic(request):
            process_function(response.message)
