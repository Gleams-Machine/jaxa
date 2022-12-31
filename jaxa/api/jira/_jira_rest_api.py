"""
Jira REST API
"""
from decouple import config
from ..jira import _jira_categories as JiraCategories
from ..rest._session import Session


class JiraRESTAPI(Session):
    def add_authorisation(self):
        self.set_basic_auth(
            username=config("JAXA_JIRA_USERNAME"),
            password=config("JAXA_JIRA_APITOKEN")
        )

    """Jira REST API"""
    @property
    def labels(self) -> JiraCategories.JiraLabels:
        """
        """
        self.add_authorisation()
        return JiraCategories.JiraLabels(self)

    @property
    def customfieldlist(self) -> JiraCategories.JiraCustomFieldList:
        """
        """
        self.add_authorisation()
        return JiraCategories.JiraCustomFieldList(self)

    @property
    def fields(self) -> JiraCategories.JiraFields:
        """
        """
        self.add_authorisation()
        return JiraCategories.JiraFields(self)

    @property
    def issues(self) -> JiraCategories.JiraIssues:
        """
        """
        self.add_authorisation()
        return JiraCategories.JiraIssues(self)

    @property
    def links(self) -> JiraCategories.JiraLinks:
        """
        """
        self.add_authorisation()
        return JiraCategories.JiraLinks(self)
