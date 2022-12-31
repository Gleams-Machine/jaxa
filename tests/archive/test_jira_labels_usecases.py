"""
Test Use Cases
"""

import datetime
import uuid
import pytest
from decouple import config


TEST_PROJECT_ID = config("JAXA_TEST_PROJECT_ID")


@pytest.mark.usecases
def test__jira_labels__add_label(jirasync_client):
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
    response = jirasync_client.jira.issues.create_issue(
        body=issue_body
    )
    print(f"Ticket created: {response.get('key')}")

    jirasync_client.jira.labels.add_label(
        ticket_id=response.get("id"),
        label="Added"
    )
    response = jirasync_client.jira.issues.get_issue(issue_id=response.get("id"))
    assert response.get("fields", {}).get("labels") == ["Added"]
