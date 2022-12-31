"""
Jira API categories
"""
from typing import Dict, Optional

from ...api.rest import HTTPMethods, MetaCategory
from ...utils import log


class JiraLabels(MetaCategory):
    def add_label(self, *, ticket_id: str, label: str) -> dict:
        """ """
        log.debug(f"Adding label [{label}] to ticket {ticket_id}")
        body = {"update": {"labels": [{"add": label}]}}
        return self._session.request(
            HTTPMethods.PUT, f"rest/api/2/issue/{ticket_id}", json=body
        )

    def remove_label(self, ticket_id: str, label: str) -> dict:
        """ """
        log.debug(f"Removing label [{label}] from ticket {ticket_id}")
        body = {"update": {"labels": [{"remove": label}]}}
        return self._session.request(
            HTTPMethods.PUT, f"rest/api/2/issue/{ticket_id}", json=body
        )


class JiraCustomFieldList(MetaCategory):
    def add_customfieldlist_item(
        self, *, ticket_id: str, item: str, custom_field_id: str
    ) -> dict:
        """ """
        log.debug(
            f"Adding [{item}] to CustomField ID {custom_field_id} on ticket {ticket_id}"
        )
        body = {"update": {custom_field_id: [{"add": item}]}}
        return self._session.request(
            HTTPMethods.PUT, f"rest/api/2/issue/{ticket_id}", json=body
        )

    def set_customfieldlist(
        self, *, ticket_id: str, items: list, custom_field_id: str
    ) -> dict:
        """ """
        log.debug(
            f"Setting CustomField ID {custom_field_id} on ticket {ticket_id} to {items}"
        )
        body = {"fields": {custom_field_id: items}}
        return self._session.request(
            HTTPMethods.PUT, f"rest/api/2/issue/{ticket_id}", json=body
        )

    def remove_customfieldlist_item(
        self, *, ticket_id: str, item: str, custom_field_id: str
    ) -> dict:
        """ """
        log.debug(
            f"Removing [{item}] from CustomField ID {custom_field_id} on ticket {ticket_id}"
        )
        body = {"update": {custom_field_id: [{"remove": item}]}}
        return self._session.request(
            HTTPMethods.PUT, f"rest/api/2/issue/{ticket_id}", json=body
        )


class JiraFields(MetaCategory):
    def get_field_id(self, *, field_name: Optional[str] = None) -> list:
        """ """
        log.debug(f"Getting all fields")
        field_list = self._session.request(HTTPMethods.GET, f"rest/api/2/field")
        if field_name is None:
            return field_list
        matched = [
            field.get("id") for field in field_list if field.get("name") == field_name
        ]
        return matched


class JiraIssues(MetaCategory):
    def create_issue(self, *, body: Dict):
        """
        Create an issue using POST
        :return:
        """
        log.debug(f"Creating issue")
        return self._session.request(HTTPMethods.POST, "rest/api/2/issue/", json=body)

    def get_issue(self, *, issue_id: str, fields: Optional[list] = None) -> dict:
        """ """
        log.debug(f"Getting issue [{issue_id}]")
        params = {}
        if fields is not None:
            params = {"fields": ",".join(fields), "expand": "renderedFields"}
        return self._session.request(
            HTTPMethods.GET, f"rest/api/2/issue/{issue_id}", params=params
        )

    def update_issue(self, *, issue_id: str, body: Dict):
        """
        Update an issue using PUT
        :return:
        """
        log.debug(f"Updating issue")
        return self._session.request(
            HTTPMethods.PUT, f"rest/api/2/issue/{issue_id}", json=body
        )


link_types = {"inward": "outward", "is tested by": "tests"}


class JiraLinks(MetaCategory):
    def get_link_types(self):
        return self._session.request(HTTPMethods.GET, f"rest/api/3/issueLinkType")

    def check_for_valid_link_type(self, name: str):
        link_types = self.get_link_types().get("issueLinkTypes")
        for link_type in link_types:
            if link_type.get("name") == name:
                return link_type
        else:
            raise Exception("Failed to find specified link type")

    def add_link(
        self, *, ticket_id: str, outward_issue_id: str, link_type: str
    ) -> dict:
        """ """
        log.debug(f"Creating link from [{ticket_id}] to [{outward_issue_id}]")
        outward_link_type = link_types.get(link_type)

        body = {
            "update": {
                "issuelinks": [
                    {
                        "add": {
                            "type": {
                                "name": "Test",
                                "inward": link_type,
                                "outward": outward_link_type,
                            },
                            "outwardIssue": {"key": outward_issue_id},
                        }
                    }
                ]
            }
        }
        return self._session.request(
            HTTPMethods.PUT, f"rest/api/2/issue/{ticket_id}", json=body
        )

    def add_jira_link(
        self, *, ticket_id: str, outward_issue_id: str, link_name: str
    ) -> dict:
        """ """
        log.debug(
            f"Creating jira link [{link_name}] from [{ticket_id}] to [{outward_issue_id}]"
        )
        link = self.check_for_valid_link_type(link_name)

        linking_body = {
            "outwardIssue": {"key": outward_issue_id},
            "inwardIssue": {"key": ticket_id},
            "type": {"name": link.get("name")},
        }
        return self._session.request(
            HTTPMethods.POST, f"rest/api/3/issueLink", json=linking_body
        )
