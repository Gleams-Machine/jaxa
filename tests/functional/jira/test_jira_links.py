"""
Functional Tests covering: Links
"""
import datetime
import uuid
import pytest
from decouple import config

pytestmark = [pytest.mark.functional]


TEST_PROJECT_ID = config("JAXA_TEST_PROJECT_ID")


@pytest.mark.xfail(True, reason="Linkage not working")
def test__jira_links__(jaxa_client):
    """

    """
    inward_link = "Contains"

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
    story_id = response.get("id")
    story_key = response.get("key")

    print(f"Ticket created: {story_key}")

    uniq = str(uuid.uuid4())[:8]
    issue_body = {
        "fields": {
            "project":
                {
                    "key": TEST_PROJECT_ID
                },
            "summary": f"Task: {uniq} [{str(datetime.datetime.now())}]",
            "description": "Creating of an issue using project keys and issue type names using the REST API",
            "issuetype": {
                "name": "Task"
            }
        }
    }
    response = jaxa_client.jira.issues.create_issue(
        body=issue_body
    )
    task_id = response.get("id")
    task_key = response.get("key")
    print(f"Ticket created: {task_key}")

    jaxa_client.jira.links.add_jira_link(ticket_id=story_id, outward_issue_id=task_id, link_name=inward_link)

    response = jaxa_client.jira.issues.get_issue(issue_id=story_id) #, fields=["links"])
    linked = [links.get("outwardIssue", {}).get("key") for links in response.get("fields", {}).get("issuelinks", [])]
    assert req_jiiraid in linked
