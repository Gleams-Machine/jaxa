"""
Jira XRay REST API
"""

from ...api.xray import _xray_categories as XRayCategories
from ...api.rest._session import Session


class XRayRESTAPI(Session):
    """XRay REST API"""

    @property
    def authenticate(self) -> XRayCategories.Authenticate:
        """
        https://xray.cloud.getxray.app/api/v1/authenticate
        Use the following API methods to authenticate.
        """
        return XRayCategories.Authenticate(self)
