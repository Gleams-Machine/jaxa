from gql.transport.requests import RequestsHTTPTransport

from ...api.graphql._gql_enums import GQLTransport


class InvalidTransportLayer(Exception):
    def __init__(self, message: str, **kwargs):
        # Call the base class constructor with the parameters it needs
        valid = [e.value for e in GQLTransport]
        message = (
            f"Invalid Transport Layer provided: {message}. Valid values are: {valid}"
        )
        super().__init__(message, kwargs)


class TransportClassFactory:
    @staticmethod
    def get_transport_class(transport_layer: GQLTransport):
        transport = transport_layer.lower()
        if transport not in [e.value for e in GQLTransport]:
            raise InvalidTransportLayer(msg=transport)

        if transport == GQLTransport.requests:
            return RequestsHTTPTransport


TransportFactory = TransportClassFactory()
