"""
Fields Use Cases
"""
import datetime
import uuid

import pytest
from decouple import config

TEST_PROJECT_ID = config("JAXA_TEST_PROJECT_ID")


@pytest.mark.usecases
def test__jira_links__add_link(jirasync_client):
    """ """
    # create a test
    uniq = str(uuid.uuid4())[:8]
    test = jirasync_client.gql.tests.create_generic_test(
        project_id=TEST_PROJECT_ID,
        summary=f"Test {uniq} [{str(datetime.datetime.now())}]",
        unstructured="",
    )
    test_jiiraid = jirasync_client.gql.tests.get_jirakeyid_from_createtest_result(test)

    # create a requirement
    requirement = jirasync_client.gql.tests.create_generic_test(
        project_id=TEST_PROJECT_ID,
        summary=f"Test {uniq} [{str(datetime.datetime.now())}]",
        unstructured="",
    )
    req_jiiraid = jirasync_client.gql.tests.get_jirakeyid_from_createtest_result(
        requirement
    )

    jirasync_client.jira.links.add_link(
        ticket_id=test_jiiraid, outward_issue_id=req_jiiraid
    )
    response = jirasync_client.jira.issues.get_issue(issue_id=test_jiiraid)
    linked = [
        links.get("outwardIssue", {}).get("key")
        for links in response.get("fields", {}).get("issuelinks", [])
    ]
    assert req_jiiraid in linked
