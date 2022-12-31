"""
Functional Tests covering: Issues
"""
import datetime
import uuid
import pytest
from decouple import config

pytestmark = [pytest.mark.functional]


TEST_PROJECT_ID = config("JAXA_TEST_PROJECT_ID")


def test__jira_issues__create_issue(jaxa_client):
    """

    """
    uniq = str(uuid.uuid4())[:8]
    issue_body = {
        "fields": {
            "project":
                {
                    "key": TEST_PROJECT_ID
                },
            "summary": f"Story: {uniq} [{str(datetime.datetime.now())}]",
            "description": "Creating of an issue using project keys and issue type names using the REST API",
            "issuetype": {
                "name": "Story"
            }
        }
    }
    response = jaxa_client.jira.issues.create_issue(
        body=issue_body
    )
    print(f"Ticket created: {response.get('key')}")
    assert response.get("key")
    assert response.get("id")
    assert response.get("self")


def test__jira_issues__get_issue(jaxa_client):
    """

    """
    uniq = str(uuid.uuid4())[:8]
    issue_body = {
        "fields": {
            "project":
                {
                    "key": TEST_PROJECT_ID
                },
            "summary": f"Story: {uniq} [{str(datetime.datetime.now())}]",
            "description": "Creating of an issue using project keys and issue type names using the REST API",
            "issuetype": {
                "name": "Story"
            }
        }
    }
    response = jaxa_client.jira.issues.create_issue(
        body=issue_body
    )
    created_id = response.get("id")
    created_key = response.get("key")
    response = jaxa_client.jira.issues.get_issue(issue_id=created_id, fields=["issuetype"])
    assert response.get("id") == created_id
    assert response.get("key") == created_key
    assert "issuetype" in list(response.get("fields", {}).keys())
    assert response.get("fields", {}).get("issuetype", {}).get("name") == "Story"


def test__jira_issues__update_issue(jaxa_client):
    """

    """
    uniq = str(uuid.uuid4())[:8]
    issue_body = {
        "fields": {
            "project":
                {
                    "key": TEST_PROJECT_ID
                },
            "summary": f"Story: {uniq} [{str(datetime.datetime.now())}]",
            "description": "Creating of an issue using project keys and issue type names using the REST API",
            "issuetype": {
                "name": "Story"
            }
        }
    }
    response = jaxa_client.jira.issues.create_issue(
        body=issue_body
    )
    created_id = response.get("id")
    created_key = response.get("key")

    update_body = {
        "fields": {
            "summary": "Issue Updated",
        }
    }
    jaxa_client.jira.issues.update_issue(issue_id=created_id, body=update_body)

    response = jaxa_client.jira.issues.get_issue(issue_id=created_id, fields=["summary"])
    assert response.get("id") == created_id
    assert response.get("key") == created_key
    assert response.get("fields", {}).get("summary") == "Issue Updated"
