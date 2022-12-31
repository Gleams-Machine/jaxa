"""
Jira ComponentList Custom Field Use Cases
"""

import datetime
import uuid
import pytest
from decouple import config


TEST_PROJECT_ID = config("JAXA_TEST_PROJECT_ID")


@pytest.mark.usecases
def test__jira_customfields__add_customfieldlist(jirasync_client):
    """

    """
    uniq = str(uuid.uuid4())[:8]
    test = jirasync_client.gql.tests.create_generic_test(
        project_id=TEST_PROJECT_ID,
        summary=f"Test {uniq} [{str(datetime.datetime.now())}]",
        unstructured=""
    )
    test_jiiraid = jirasync_client.gql.tests.get_jirakeyid_from_createtest_result(test)

    jirasync_client.jira.customfieldlist.add_customfieldlist_item(
        ticket_id=test_jiiraid,
        item="Demo",
        custom_field_id="customfield_10798",    # QA Test Levels field
    )
    response = jirasync_client.jira.issues.get_issue(issue_id=test_jiiraid, fields=["customfield_10798"])
    assert response.get("key") == test_jiiraid
    assert "customfield_10798" in list(response.get("fields").keys())
    assert response.get("fields", {}).get("customfield_10798") == ["Demo"]
