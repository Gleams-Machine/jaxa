"""
Jira And Xray API Client
"""
from typing import Optional, Union

from decouple import config

from .api.jira import JiraRESTAPI
from .api.xray import (
    AsyncTransport,
    Transport,
    TransportFactory,
    XRayGraphQLAPI,
    XRayRESTAPI,
)
from .utils import log

DEFAULT_TRANSPORT_LAYER = "Requests"


class JAXAClient:
    """JAXA Client uses both XRay REST and XRay GraphQL api's"""

    def __init__(
        self,
        jira_url: Optional[str] = None,
        rest_url: Optional[str] = None,
        transport: Optional[Union[Transport, AsyncTransport]] = None,
        **kwargs,
    ):
        self.auth_token = None
        self._init_jira_rest_api_client(rest_url=jira_url, **kwargs)
        self._init_xray_rest_api_client(rest_url=rest_url, **kwargs)
        self._init_xray_graphql_qpi_client(transport=transport, **kwargs)

    def _init_jira_rest_api_client(self, jira_url: Optional[str] = None, **kwargs):
        log.debug("Initialising internal Jira REST api client")
        self._jira = JiraRESTAPI(
            url=jira_url or config("JAXA_JIRA_REST_BASEURL"), **kwargs
        )

    def _init_xray_rest_api_client(self, rest_url: Optional[str] = None, **kwargs):
        log.debug("Initialising internal XRay REST api client")
        self._rest = XRayRESTAPI(
            url=rest_url or config("JAXA_XRAY_REST_BASEURL"), **kwargs
        )

    def _init_xray_graphql_qpi_client(
        self,
        transport: Optional[Union[Transport, AsyncTransport]] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        **kwargs,
    ):
        log.debug("Initialising internal gql api client")
        self._gql_headers = {}
        if "gql_headers" in list(kwargs.keys()):
            self._gql_headers.update(kwargs.get("gql_headers"))

        # TODO: If no client id or secret then raise exception
        self._gql_headers.update(
            self.gql_auth_header(client_id=client_id, client_secret=client_secret)
        )

        if transport is None:
            self._transport = TransportFactory.get_transport_class(
                DEFAULT_TRANSPORT_LAYER
            )(url=config("JAXA_XRAY_GQL_BASEURL"), headers=self._gql_headers)
        else:
            self._transport = transport
        self._qgl = XRayGraphQLAPI(self._transport, **kwargs)

    @property
    def jira(self):
        return self._jira

    # deprecated
    @property
    def rest(self):
        return self._rest

    @property
    def xray_rest(self):
        return self._rest

    # deprecated
    @property
    def gql(self):
        return self._qgl

    @property
    def xray_gql(self):
        return self._qgl

    def gql_auth_header(
        self, client_id: Optional[str] = None, client_secret: Optional[str] = None
    ):
        self.auth_token = self._rest.authenticate.get_auth_token(
            client_id=client_id, client_secret=client_secret
        )
        return {"Authorization": f"Bearer {self.auth_token}"}
