"""
Fields Use Cases
"""

import pytest


@pytest.mark.jira
@pytest.mark.fields
@pytest.mark.usecases
def test__jira_fields__get_all_fields(jirasync_client):
    """

    """
    response = jirasync_client.jira.fields.get_field_id()
    parent = [field for field in response if field.get("name") == "Parent"]
    assert parent[0].get("id") == "parent"


@pytest.mark.jira
@pytest.mark.fields
@pytest.mark.usecases
def test__jira_fields__get_custom_field(jirasync_client):
    """

    """
    response = jirasync_client.jira.fields.get_field_id(
        field_name="QA_Test_Levels"
    )
    assert len(response) == 1
