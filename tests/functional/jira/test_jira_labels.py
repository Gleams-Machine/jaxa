"""
Functional Tests covering: Labels
"""
import datetime
import uuid
import pytest
from decouple import config

pytestmark = [pytest.mark.functional]


TEST_PROJECT_ID = config("JAXA_TEST_PROJECT_ID")


def test__jira_labels__add_label(jaxa_client):
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

    print(f"Ticket created: {created_key}")
    jaxa_client.jira.labels.add_label(
        ticket_id=created_id,
        label="Added"
    )
    response = jaxa_client.jira.issues.get_issue(issue_id=created_id, fields=["labels"])
    assert response.get("fields", {}).get("labels") == ["Added"]


def test__jira_labels__add_multiple_labels(jaxa_client):
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

    print(f"Ticket created: {created_key}")
    multi_labels = ["Multiple", "Labels", "Added"]
    for label in multi_labels:
        jaxa_client.jira.labels.add_label(
            ticket_id=created_id,
            label=label
        )
    response = jaxa_client.jira.issues.get_issue(issue_id=created_id, fields=["labels"])
    assert sorted(response.get("fields", {}).get("labels")) == sorted(multi_labels)


def test__jira_labels__remove_label(jaxa_client):
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

    print(f"Ticket created: {created_key}")
    jaxa_client.jira.labels.add_label(
        ticket_id=created_id,
        label="Added"
    )
    jaxa_client.jira.labels.remove_label(
        ticket_id=created_id,
        label="Added"
    )
    response = jaxa_client.jira.issues.get_issue(issue_id=created_id, fields=["labels"])
    assert response.get("fields", {}).get("labels") == []
