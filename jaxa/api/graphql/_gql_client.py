from gql import Client, gql
from typing import Optional, Union
from gql.transport import AsyncTransport, Transport


class GQLAPIClient:
    def __init__(
            self,
            transport_layer: Optional[Union[Transport, AsyncTransport]] = None,
            fetch_schema_from_transport: bool = True
    ) -> None:
        # Create a GraphQL client using the defined transport
        self.client = Client(transport=transport_layer, fetch_schema_from_transport=fetch_schema_from_transport)

    def execute_query(self, query: str, variables: Optional[dict] = None) -> dict:
        return self.client.execute(gql(query), variable_values=variables)
